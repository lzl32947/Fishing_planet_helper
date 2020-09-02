import global_configs
from PIL import Image

from dependence.utils import hwnd_util
from gui.hwnd_select_gui import show_all_hwnd_select_gui
from log import logger


def init_ram():
    global_configs.wheel_image = Image.open("image/wheel.png")
    global_configs.get_image = Image.open("image/get.png")
    global_configs.full_image = Image.open("image/full.png")
    global_configs.special_event_image = Image.open("image/special_event.png")
    global_configs.xp_confirm_image = Image.open("image/xp.png")


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
