from configs import global_configs
from PIL import Image

from dependence.utils import hwnd_util
from gui.hwnd_select_gui import show_all_hwnd_select_gui
from log import logger


def init_ram():
    global_configs.wheel_image = Image.open("image/buttons/wheel.png")
    global_configs.get_image = Image.open("image/buttons/get.png")
    global_configs.full_image = Image.open("image/buttons/full.png")
    global_configs.special_event_image = Image.open("image/buttons/special_event.png")
    global_configs.xp_confirm_image = Image.open("image/buttons/xp.png")

    global_configs.digit_0_image = Image.open("image/distance/0_grey.png")
    global_configs.digit_1_image = Image.open("image/distance/1_grey.png")
    global_configs.digit_2_image = Image.open("image/distance/2_grey.png")
    global_configs.digit_3_image = Image.open("image/distance/3_grey.png")
    global_configs.digit_4_image = Image.open("image/distance/4_grey.png")
    global_configs.digit_5_image = Image.open("image/distance/5_grey.png")
    global_configs.digit_6_image = Image.open("image/distance/6_grey.png")
    global_configs.digit_7_image = Image.open("image/distance/7_grey.png")
    global_configs.digit_8_image = Image.open("image/distance/8_grey.png")
    global_configs.digit_9_image = Image.open("image/distance/9_grey.png")


def init_config():
    init_ram()
    logger.info("Image init complete.")
    hwnd = show_all_hwnd_select_gui()
    if hwnd is None:
        raise RuntimeError("No hWnd Selected.")
    global_configs.hwnd = hwnd
    x0, y0, x1, y1 = hwnd_util.get_window_position(hwnd)
    global_configs.windows_x = x0
    global_configs.windows_y = y0
    global_configs.windows_width = x1 - x0
    global_configs.windows_height = y1 - y0

    logger.info("Configs init complete.")
    logger.info(
        "Application location:{}, {}, {}, {}.".format(global_configs.windows_x, global_configs.windows_y,
                                                      global_configs.windows_x + global_configs.windows_width,
                                                      global_configs.windows_y + global_configs.windows_height))
