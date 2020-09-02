import win32gui, win32api, win32con, win32ui
import PySimpleGUI as sg


def list_all_hwnd():
    result = []
    hwnd_title = dict()

    def get_all_hwnd(hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

    win32gui.EnumWindows(get_all_hwnd, 0)
    for h, t in hwnd_title.items():
        if t is not "":
            result.append((h, t))
    return result


def get_window_title(hwnd):
    return win32gui.GetWindowText(hwnd)


def get_window_class(hwnd):
    return win32gui.GetClassName(hwnd)


def get_window_position(hwnd):
    return win32gui.GetWindowRect(hwnd)


def get_window_size(hwnd):
    xmin, ymin, xmax, ymax = get_window_position(hwnd)
    return xmax - xmin, ymax - ymin


def find_child_hwnd(parent_hwnd):
    hwndChildList = []
    result_list = []
    win32gui.EnumChildWindows(parent_hwnd, lambda hwnd, param: param.append(hwnd), hwndChildList)
    for item in hwndChildList:
        result_list.append((item,get_window_title(item), get_window_class(item), get_window_size(item)))

    return result_list
