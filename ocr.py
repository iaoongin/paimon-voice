import easyocr
import warnings
from util import log_factory
from util.timing import timing
from win32gui import FindWindow, GetWindowRect, GetForegroundWindow
from PIL import Image, ImageGrab
import ctypes
import time
import io
import threading

class OCRThread(threading.Thread):

    def __init__(self, queue) -> None:
        super().__init__()
        self.queue = queue
        self.thread = None
        self.load_easyocr()
        pass

    def load_easyocr(self):
        warnings.filterwarnings("ignore", category=UserWarning)

        # this needs to run only once to load the model into memory
        global reader
        reader = easyocr.Reader(['ch_sim', 'en'])

    def read(self, image):

        result = reader.readtext(image, detail=0)

        return result

    def find_win(self, title):
        # FindWindow takes the Window Class name (can be None if unknown), and the window's display text.
        window_handle = FindWindow(None, title)

        # 获取当前激活的窗口句柄
        foreground_hwnd = GetForegroundWindow()

        # # 判断是否为激活的窗口
        # if window_handle == foreground_hwnd:
        #     print('目标窗口正在被使用')
        # else:
        #     print('目标窗口未被使用')
        #     return None

        # window_rect   = GetWindowRect(window_handle)
        # win32gui.GetWindowRect() 取值不准的解决方案 https://blog.csdn.net/See_Star/article/details/103940462

        try:
            f = ctypes.windll.dwmapi.DwmGetWindowAttribute
        except WindowsError:
            f = None
        if f:
            rect = ctypes.wintypes.RECT()
            DWMWA_EXTENDED_FRAME_BOUNDS = 9
            f(ctypes.wintypes.HWND(window_handle),
            ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
            ctypes.byref(rect),
            ctypes.sizeof(rect)
            )
            window_rect = (rect.left, rect.top, rect.right, rect.bottom)

        # LOG.info(window_rect)
        #(0, 0, 800, 600)
        return window_rect

    def get_subtitle_rect(self, bbox):
        """
            获取字幕所在位置
        """
        # 修改元组
        top = bbox[1]
        bottom = bbox[3]

        new_top = bottom - (bottom - top) / 4

        return (bbox[0], new_top, bbox[2], bottom - 60)

    def capture(self, bbox=None):
        # im1 = ImageGrab.grab()  # 截屏操作 默认全屏
        im1 = ImageGrab.grab(
            bbox=bbox, include_layered_windows=False, all_screens=True)

        #  保存图片
        # TimeName = time.strftime("%Y%m%d%H%M%S", time.localtime())  # 通过时间命名
        # path = '.\\capture\\'+str(TimeName)+'.jpg'
        # im1.save(path)

        b = io.BytesIO()

        # 设置压缩质量为50%
        compression_quality = 50

        im1.save(b, 'JPEG', quality=compression_quality)

        im1.close()

        im_bytes = b.getvalue()

        return im_bytes
        # im1.show()  # 展示

    def run(self):

        LOG = log_factory.getReadLog()

        LOG.info("# 开启识图进程")

        while (True):

            raw_bbox = self.find_win('原神')

            if raw_bbox is None:
                time.sleep(1)
                continue

            bbox = self.get_subtitle_rect(raw_bbox)

            img = timing(self.capture, bbox, '截图')

            # img_size = len(img) / 1024
            # LOG.info("图片大小: %s kb" % img_size+"")

            # r = timing(self.read, img, '解析文字', LOG)
            r = timing(self.read, img, '解析文字')

            # LOG.info("结果: %s" % r)

            if r:
                self.queue.put(r)

            time.sleep(1)
    