from PIL import ImageGrab
import pygetwindow as gw
import win32gui
import ctypes

def get_window_rect(window_title):
    def callback(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd) and window_title in win32gui.GetWindowText(hwnd):
            rect = win32gui.GetWindowRect(hwnd)
            
            # win32gui.GetWindowRect() 取值不准的解决方案 https://blog.csdn.net/See_Star/article/details/103940462
            try:
                f = ctypes.windll.dwmapi.DwmGetWindowAttribute
            except WindowsError:
                f = None
            if f:
                rect = ctypes.wintypes.RECT()
                DWMWA_EXTENDED_FRAME_BOUNDS = 9
                f(ctypes.wintypes.HWND(hwnd),
                ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
                ctypes.byref(rect),
                ctypes.sizeof(rect)
                )
            window_rect = (rect.left, rect.top, rect.right, rect.bottom)
            windows.append(window_rect)

    windows = []
    win32gui.EnumWindows(callback, None)
    return windows[0] if windows else None

def screenshot(window_title=None, save_path='screenshot.png'):
    if window_title:
        rect = get_window_rect(window_title)
        if rect:
            bbox = (rect[0], rect[1], rect[2], rect[3])
        else:
            print(f"Window with title '{window_title}' not found.")
            return
    else:
        bbox = None

    img = ImageGrab.grab(bbox)
    img.save(save_path)
    # img.show()
