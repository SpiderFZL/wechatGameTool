from ctypes import windll, byref, c_ubyte
import win32gui
import pyautogui
import cv2  # https://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv
import numpy as np
GetDC = windll.user32.GetDC
CreateCompatibleDC = windll.gdi32.CreateCompatibleDC
GetClientRect = windll.user32.GetClientRect
CreateCompatibleBitmap = windll.gdi32.CreateCompatibleBitmap
SelectObject = windll.gdi32.SelectObject
BitBlt = windll.gdi32.BitBlt
SRCCOPY = 0x00CC0020
GetBitmapBits = windll.gdi32.GetBitmapBits
DeleteObject = windll.gdi32.DeleteObject
ReleaseDC = windll.user32.ReleaseDC
pyautogui.FAILSAFE=False
# 排除缩放干扰
windll.user32.SetProcessDPIAware()


def capture(start_y=None, end_y=None, save_name='my_screenshot.png'):
    hwnd1 = win32gui.FindWindow(None, '万剑诀')
    rect = win32gui.GetWindowRect(hwnd1)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    if start_y is None:
        start_y = 0
    y = y + start_y
    if end_y is not None:
        h = end_y - start_y
    img = pyautogui.screenshot(region=[x, y, w, h])  # x,y,w,h

    img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)  # cvtColor用于在图像中不同的色彩空间进行转换,用于后续处理。
    cv2.imwrite(save_name, img)
    return x, y, w, h


if __name__ == "__main__":
    hwnd = win32gui.FindWindow(None, '万剑诀')
    capture(hwnd)
