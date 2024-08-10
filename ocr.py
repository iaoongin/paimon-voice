import easyocr
import warnings
from util import log_factory
from util.screenshot import get_window_rect
from util.timing import timing
from win32gui import *
from PIL import Image, ImageGrab
import ctypes
import time
import io
import threading

class OCRThread(threading.Thread):

    def __init__(self, queue) -> None:
        super().__init__()
        self.log = log_factory.getReadLog()
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

    def get_subtitle_rect(self, bbox):
        """
            获取字幕所在位置
        """
        self.log.debug(f'获取字幕所在位置, 原始bbox: {bbox}')
        # 修改元组
        top = bbox[1]
        bottom = bbox[3]

        new_top = bottom - (bottom - top) / 4

        return (bbox[0], new_top, bbox[2], bottom - 60)

    def capture(self, bbox=None):
        # im1 = ImageGrab.grab()  # 截屏操作 默认全屏
        self.log.debug(f'开始截屏： {bbox}')
        im1 = ImageGrab.grab(
            bbox=bbox, include_layered_windows=False, all_screens=True)

        #  保存图片
        TimeName = time.strftime("%Y%m%d%H%M%S", time.localtime())  # 通过时间命名
        path = '.\\capture\\'+str(TimeName)+'.jpg'
        im1.save(path)

        b = io.BytesIO()

        # 设置压缩质量为50%
        compression_quality = 50

        im1.save(b, 'JPEG', quality=compression_quality)

        im1.close()

        im_bytes = b.getvalue()

        return im_bytes
        # im1.show()  # 展示

    def run(self):

        self.log.info("# 开启识图进程")

        while (True):

            # raw_bbox = self.find_win('原神')
            raw_bbox = get_window_rect('崩坏：星穹铁道')
            if raw_bbox is None:
                time.sleep(1)
                continue

            bbox = self.get_subtitle_rect(raw_bbox)

            img = timing(self.capture, bbox, '截图')

            img_size = len(img) / 1024
            self.log.debug("图片大小: %s kb" % img_size+"")

            # r = timing(self.read, img, '解析文字', LOG)
            r = timing(self.read, img, '解析文字', self.log)

            self.log.debug("结果: %s" % r)

            if r:
                self.queue.put(r)

            time.sleep(1)
    