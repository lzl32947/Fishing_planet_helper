import os

import PySimpleGUI as sg

from configs.file_configs import RUNTIME_SCREENSHOT_DIR, IMAGE_NN_DIR
from configs.image_config import CropImageCollection, CropImage
from dependence.utils.hwnd_util import list_all_hwnd
from dependence.utils.image_process_util import crop_screenshot_by_class, crop_screenshot_by_tuple
from dependence.utils.screenshot_util import take_screenshot_of_program_using_win32api


def take_screenshot_gui(hwnd):
    des_list = []
    dicts = CropImageCollection().image_dict

    for key in dicts:
        item: CropImage = dicts[key]
        describe = item.describe
        s = "{}:{}".format(key, describe)
        des_list.append(s)

    listbox_element = sg.Listbox(values=des_list, size=(50, 10))
    text_element = sg.InputText(default_text="", size=(10, 10))
    layout = [[sg.Text('Please select the cropped area that you want to take screenshot')],
              [sg.Text('请输入要拍摄屏幕快照的剪裁位置')],
              [listbox_element],
              [text_element],
              [sg.Button('Ok'), sg.Button('Cancel')]]

    select = None
    count = 0
    window = sg.Window('Screenshot', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        elif event == "Ok":
            select = values[0][0].split(":")[0]
            if not select:
                continue
            else:
                take_screenshot_of_program_using_win32api(hwnd, RUNTIME_SCREENSHOT_DIR)
                image_object = CropImageCollection().image_dict[select]
                image = crop_screenshot_by_class(RUNTIME_SCREENSHOT_DIR, image_object,
                                                 save_image=True, use_custom_name=True, custom_name="test")
    window.close()


def take_screenshot_for_route_training(hwnd, start_id):
    path = os.path.join(IMAGE_NN_DIR, "{:0>5d}.png".format(start_id))
    if os.path.exists(path):
        raise RuntimeError("image already exist!")
    layout = [[sg.Text('Press OK to take screenshot of route area:(150,200) to (1600,800)')],
              [sg.Text('点击"OK"拍摄用于训练的路径区域')],

              [sg.Button('Ok'), sg.Button('Cancel')]]

    window = sg.Window('Route Screenshot', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        elif event == "Ok":
            take_screenshot_of_program_using_win32api(hwnd, RUNTIME_SCREENSHOT_DIR)
            crop_screenshot_by_tuple(RUNTIME_SCREENSHOT_DIR, (150, 200, 1600, 800), path
                                     )
            start_id += 1
    window.close()
