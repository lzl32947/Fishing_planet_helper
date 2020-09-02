from ctypes import Structure, sizeof, memmove, pointer, memset
from ctypes.wintypes import WORD, DWORD, LONG
import win32clipboard
import sys, time
import win32api, win32con


class KeyboardAction(object):
    @classmethod
    def press_and_release(cls, key, delay_time=0.3, in_hex=True):
        win32api.keybd_event(key, 0, 0, 0)
        time.sleep(delay_time)
        win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)
