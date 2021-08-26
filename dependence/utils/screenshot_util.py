import win32gui, win32con, win32ui
from PIL import Image, ImageGrab


def take_screenshot_of_program_using_win32api(hwnd, save_name):
    hwnd_target = hwnd
    left, top, right, bot = win32gui.GetWindowRect(hwnd_target)
    w = right - left
    h = bot - top

    win32gui.SetForegroundWindow(hwnd_target)

    hdesktop = win32gui.GetDesktopWindow()
    hwndDC = win32gui.GetWindowDC(hdesktop)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    result = saveDC.BitBlt((0, 0), (w, h), mfcDC, (left, top), win32con.SRCCOPY)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hdesktop, hwndDC)

    if result == None:
        # PrintWindow Succeeded
        im.save(save_name)


def take_screenshot_of_desktop_using_PIL(window_x, window_y,
                                         relative_crop_box=None):
    image = ImageGrab.grab()
    if relative_crop_box:
        image = image.crop((window_x + relative_crop_box[0], window_y + relative_crop_box[1],
                            window_x + relative_crop_box[2], window_y + relative_crop_box[3]))
    return image
