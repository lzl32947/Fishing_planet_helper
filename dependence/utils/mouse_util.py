import time

import numpy as np
import win32api
import win32con
import win32gui


class MouseAction(object):
    @classmethod
    def click(cls, x, y):
        original_position = win32api.GetCursorPos()
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        win32api.SetCursorPos(original_position)

    @classmethod
    def click_with_delay(cls, x, y, delay_time=0.4):
        win32api.SetCursorPos((x, y))
        time.sleep(delay_time)
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(delay_time / 2)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


    @classmethod
    def right_click(cls, x, y):
        original_position = win32api.GetCursorPos()
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
        win32api.SetCursorPos(original_position)

    @classmethod
    def left_long_click(cls, x, y, sleep_time=1):
        original_position = win32api.GetCursorPos()
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(sleep_time)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        win32api.SetCursorPos(original_position)

    @classmethod
    def drag(cls, x1, y1, x2, y2):
        original_position = win32api.GetCursorPos()
        screen_x = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        screen_y = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        start_x = x1 * 65535 // screen_x
        start_y = y1 * 65535 // screen_y
        dst_x = x2 * 65535 // screen_x
        dst_y = y2 * 65535 // screen_y
        move_x = np.linspace(start_x, dst_x, num=20, endpoint=True)[0:]
        move_y = np.linspace(start_y, dst_y, num=20, endpoint=True)[0:]
        start_x = np.array([move_x[0]] * 5)
        start_y = np.array([move_y[0]] * 5)
        stop_x = np.array([move_x[-1]] * 5)
        stop_y = np.array([move_y[-1]] * 5)
        move_y = np.concatenate((start_y, move_y, stop_y))
        move_x = np.concatenate((start_x, move_x, stop_x))
        win32api.SetCursorPos((x1, y1))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        for i in range(20):
            x = int(round(move_x[i]))
            y = int(round(move_y[i]))
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, x, y, 0, 0)
            time.sleep(0.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        win32api.SetCursorPos(original_position)

    @classmethod
    def drag_with_hwnd(cls, hwnd, x1, y1, x2, y2):
        original_position = win32api.GetCursorPos()
        pos1_s = win32gui.ClientToScreen(hwnd, (x1, y1))
        pos2_s = win32gui.ClientToScreen(hwnd, (x2, y2))
        screen_x = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        screen_y = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        start_x = pos1_s[0] * 65535 // screen_x
        start_y = pos1_s[1] * 65535 // screen_y
        dst_x = pos2_s[0] * 65535 // screen_x
        dst_y = pos2_s[1] * 65535 // screen_y
        move_x = np.linspace(start_x, dst_x, num=20, endpoint=True)[0:]
        move_y = np.linspace(start_y, dst_y, num=20, endpoint=True)[0:]
        start_x = np.array([move_x[0]] * 5)
        start_y = np.array([move_y[0]] * 5)
        stop_x = np.array([move_x[-1]] * 5)
        stop_y = np.array([move_y[-1]] * 5)
        move_y = np.concatenate((start_y, move_y, stop_y))
        move_x = np.concatenate((start_x, move_x, stop_x))
        win32api.SetCursorPos(pos1_s)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        for i in range(len(move_x)):
            x = int(round(move_x[i]))
            y = int(round(move_y[i]))
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, x, y, 0, 0)
            time.sleep(0.05)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        win32api.SetCursorPos(original_position)

    @classmethod
    def hold_on_right_then_left(cls, x, y, right_hold_time=1, both_hold_time=3):
        original_position = win32api.GetCursorPos()
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
        time.sleep(right_hold_time)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(both_hold_time)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
        win32api.SetCursorPos(original_position)
