import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2


def crop_screenshot_by_tuple(file_path: str, crop_area: tuple, image_save_path: str):
    img = Image.open(file_path)
    cropped = img.crop(crop_area)
    cropped.save(image_save_path)


def image_diff(raw_image: Image, other_image: Image, function: str = None):
    raw_image = np.array(raw_image)
    other_image = np.array(other_image)

    def _hist(img1, img2):
        H1 = cv2.calcHist([img1], [1], None, [256], [0, 256])
        H1 = cv2.normalize(H1, H1, 0, 1, cv2.NORM_MINMAX, -1)

        H2 = cv2.calcHist([img2], [1], None, [256], [0, 256])
        H2 = cv2.normalize(H2, H2, 0, 1, cv2.NORM_MINMAX, -1)
        return cv2.compareHist(H1, H2, 0)

    if raw_image.shape != other_image.shape:
        raise RuntimeWarning("Warning: image shape not equal !")
    else:
        if function is None or function.lower() == "hist":
            return _hist(raw_image, other_image)


def find_pattern_in_image(raw_image_path: str, pattern_path: str, function: str = None, threshold: float = 0.5,
                          include_nms=True, plot_image=False):
    def nms(bounding_boxes, confidence_score, nms_threshold):
        if len(bounding_boxes) == 0:
            return [], []

        boxes = np.array(bounding_boxes)

        start_x = boxes[:, 0]
        start_y = boxes[:, 1]
        end_x = boxes[:, 2]
        end_y = boxes[:, 3]

        score = np.array(confidence_score)

        picked_boxes = []
        picked_score = []

        areas = (end_x - start_x + 1) * (end_y - start_y + 1)

        order = np.argsort(score)
        while order.size > 0:
            index = order[-1]
            picked_boxes.append(bounding_boxes[index])
            picked_score.append(confidence_score[index])

            x1 = np.maximum(start_x[index], start_x[order[:-1]])
            x2 = np.minimum(end_x[index], end_x[order[:-1]])
            y1 = np.maximum(start_y[index], start_y[order[:-1]])
            y2 = np.minimum(end_y[index], end_y[order[:-1]])

            w = np.maximum(0.0, x2 - x1 + 1)
            h = np.maximum(0.0, y2 - y1 + 1)
            intersection = w * h

            ratio = intersection / (areas[index] + areas[order[:-1]] - intersection)
            left = np.where(ratio < nms_threshold)
            order = order[left]
        return picked_boxes, picked_score

    raw_image = cv2.imread(raw_image_path, cv2.IMREAD_COLOR)
    pattern = cv2.imread(pattern_path, cv2.IMREAD_COLOR)
    shape = pattern.shape
    if function is None or function.lower() == "sqdiffn":
        res = cv2.matchTemplate(raw_image, pattern, cv2.TM_SQDIFF_NORMED)
    elif function.lower() == "ccorr":
        res = cv2.matchTemplate(raw_image, pattern, cv2.TM_CCORR)
    elif function.lower() == "ccoeff":
        res = cv2.matchTemplate(raw_image, pattern, cv2.TM_CCOEFF)
    elif function.lower() == "sqdiff":
        res = cv2.matchTemplate(raw_image, pattern, cv2.TM_SQDIFF)
    elif function.lower() == "ccorrn":
        res = cv2.matchTemplate(raw_image, pattern, cv2.TM_CCORR_NORMED)
    elif function.lower() == "ccoeffn":
        res = cv2.matchTemplate(raw_image, pattern, cv2.TM_CCOEFF_NORMED)
    else:
        raise RuntimeWarning("No match method selected!")

    k = np.where(res[:, :] < threshold)
    box = []
    conf = []
    for (x, y) in zip(k[1], k[0]):
        box.append([x, y, x + shape[1], y + shape[1]])
        conf.append(1 - res[y, x])
    if include_nms:
        box, conf = nms(box, conf, 1 - threshold)
    if plot_image:
        plt.figure()
        plt.imshow(raw_image[:, :, :: -1])
        for p in box:
            plt.gca().add_patch(
                plt.Rectangle((p[0], p[1]), p[2] - p[0],
                              p[3] - p[1], fill=False,
                              edgecolor='r', linewidth=1))
        plt.show()
        plt.close()
    return box, conf
