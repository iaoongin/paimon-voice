import ctypes
import hashlib
import io
import logging
import os
import signal
# 文本相似度
import sys
import threading
import time
import warnings
from difflib import SequenceMatcher
from email.mime import image
from multiprocessing import Pool
from queue import Queue

import easyocr
import pyttsx3
from PIL import Image, ImageGrab
from sentence_transformers import SentenceTransformer as SBert
from sentence_transformers.util import cos_sim
from win32gui import FindWindow, GetWindowRect
import numpy as np


def load_easyocr():
    warnings.filterwarnings("ignore", category=UserWarning)

    # this needs to run only once to load the model into memory
    global reader
    reader = easyocr.Reader(['ch_sim', 'en'])


def timing(fun, args=None, title=''):
    s = time.time()

    if args:
        r = fun(args)
    else:
        r = fun()
    e = time.time()

    LOG.info('%scost: %s' % (title+' ', (e-s)))
    return r


def read(image):

    result = reader.readtext(image, detail=0)

    return result


def check_cuda():
    import torch
    LOG.info(torch.zeros(1).cuda())
    LOG.info(torch.cuda.is_available())


# lock = threading.Lock()


def say(text):

    # lock.acquire()
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate+50)

    engine.say(text)

    # if not engine.isBusy():

    engine.runAndWait()

    # LOG.info('after say.')
    # lock.release()


def md5(data):
    return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()


def find(s, c):

    if isinstance(c, list):
        for v in c:
            if v in s:
                return True
        return False
    else:
        return c in s

# 判断是否为数字


def is_number(s):
    try:    # 如果能运⾏ float(s) 语句，返回 True（字符串 s 是浮点数）
        float(s)
        return True
    except ValueError:  # ValueError 为 Python 的⼀种标准异常，表⽰"传⼊⽆效的参数"
        pass  # 如果引发了 ValueError 这种异常，不做任何事情（pass：不做任何事情，⼀般⽤做占位语句）
    try:
        import unicodedata  # 处理 ASCII 码的包
        unicodedata.numeric(s)  # 把⼀个表⽰数字的字符串转换为浮点数返回的函数
        return True
    except (TypeError, ValueError):
        pass
        return False


def is_contain_chinese(check_str):
    """
    判断字符串中是否包含中文
    :param check_str: {str} 需要检测的字符串
    :return: {bool} 包含返回True， 不包含返回False
    """
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


said_text = dict()
sentences1 = np.array([''])
queue = Queue(100)
model = SBert('./model/paraphrase-multilingual-MiniLM-L12-v2')


def samrt_say(text):

    global sentences1
    global RATIO

    if not isinstance(text, list):
        LOG.info(type(text) + ', 不支持的类型')
        return

    text = [v for v in text if is_contain_chinese(v) and not (
        find(v, ['ID', 'UID', 'Lv', 'LV', 'Enter',
             'E', 'Q', 'R', '保存配置', '快速列队', '活动']) or is_number(v)
    )]

    sentences2 = np.array([','.join(text)])

    LOG.info("sentences1: %s" % sentences1)
    LOG.info("sentences2: %s" % sentences2)

    # ratio = SequenceMatcher(None, tmp_text['1'], text).ratio()

    # Compute embedding for both lists
    embeddings1 = model.encode(sentences1)
    embeddings2 = model.encode(sentences2)

    # Compute cosine-similarits
    cosine_scores = cos_sim(embeddings1, embeddings2)
    # cosine_scores_diag = cosine_scores.diag()
    ratio = cosine_scores.mean().float()

    # LOG.info('相似度: %s' % (str(cosine_scores)))
    # LOG.info('相似度: %s' % (str(cosine_scores_diag)))
    LOG.info('model相似度: %s' % (str(ratio)))
    # LOG.info('相似度:' + str(ratio))
    # LOG.info('相似度:' + str(cosine_scores.mean()))
    # for i in range(len(text)):
    # LOG.info("{} \t\t {} \t\t Score: {:.4f}".format('1', '2', cosine_scores[i][i]))

    # difflib 相似度
    s = SequenceMatcher(None, sentences1[0], sentences2[0])
    ratio2 = s.ratio()
    LOG.info('difflib相似度: %s' % (str(ratio2)))

    if (ratio > RATIO and ratio2 > RATIO):
        return

    LOG.info("刷新缓存sentences1...")
    sentences1 = sentences2

    for t in text:
        if "UID" in t:
            continue
        if "ID" in t:
            continue

        LOG.info("添加到朗读队列...")
        queue.put(t)


def capture(bbox=None):
    # im1 = ImageGrab.grab()  # 截屏操作 默认全屏
    im1 = ImageGrab.grab(
        bbox=bbox, include_layered_windows=False, all_screens=True)

    #  保存图片
    # TimeName = time.strftime("%Y%m%d%H%M%S", time.localtime())  # 通过时间命名
    # path = '.\\capture\\'+str(TimeName)+'.jpg'
    # im1.save(path)

    b = io.BytesIO()
    im1.save(b, 'jpeg')

    im1.close()

    im_bytes = b.getvalue()

    return im_bytes
    # im1.show()  # 展示


def find_win(title):
    # FindWindow takes the Window Class name (can be None if unknown), and the window's display text.
    window_handle = FindWindow(None, title)

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

    LOG.info(window_rect)
    #(0, 0, 800, 600)
    return window_rect


def get_subtitle_rect(bbox):
    # 修改元组
    top = bbox[1]
    bottom = bbox[3]

    new_top = bottom - (bottom - top) / 4

    return (bbox[0], new_top, bbox[2], bottom - 60)

# check_cuda()


# load()


# r = read('./test/2.png')
# say(r)

# r = read('./test/1.png')
# say(r)


# load()
# img = timing(capture)
# r = read(img)

# LOG.info(r)

# say(r)

    # time.sleep(1)

# say(r)

def read_thread():

    LOG.info("# 开启识图进程")

    while (True):

        raw_bbox = find_win('原神')
        bbox = get_subtitle_rect(raw_bbox)

        img = timing(capture, bbox, '截图')
        r = timing(read, img, '解析文字')

        samrt_say(r)

        time.sleep(1)


def say_thread():

    LOG.info("# 开启朗读进程")

    while (True):

        r = queue.get()
        LOG.info(r)
        
        try:
            say(r)
        except Exception as e:
            LOG.error(e)


def exit(a, b):
    LOG.info('###########################')
    LOG.info('# ')
    LOG.info('# 退出派蒙语音')
    LOG.info('# ')
    LOG.info('###########################')
    os.kill(os.getpid(), signal.SIGILL)


def init_log():

    global LOG

    # 第一步，创建一个logger

    LOG = logging.getLogger('派蒙语音')

    LOG.setLevel(logging.INFO)  # Log等级总开关

    # 第二步，创建一个handler，用于写入日志文件
    logfile = './log.txt'

    fh = logging.FileHandler(
        logfile, mode='a', encoding='utf8')  # open的打开模式这里可以进行参考

    fh.setLevel(logging.INFO)  # 输出到file的log等级的开关

    # 第三步，再创建一个handler，用于输出到控制台

    ch = logging.StreamHandler()

    ch.setLevel(logging.INFO)  # 输出到console的log等级的开关

    # 第四步，定义handler的输出格式

    formatter = logging.Formatter(
        "%(asctime)s - %(filename)s[line:%(lineno)3d] - %(levelname)s: %(message)s")

    fh.setFormatter(formatter)

    ch.setFormatter(formatter)

    # 第五步，将logger添加到handler里面

    LOG.addHandler(fh)

    LOG.addHandler(ch)


if __name__ == "__main__":

    init_log()

    LOG.info('###########################')
    LOG.info('# ')
    LOG.info('# 启动派蒙语音')
    LOG.info('# ')
    LOG.info('###########################')

    signal.signal(signal.SIGINT, exit)
    signal.signal(signal.SIGTERM, exit)

    global RATIO
    RATIO = 0.6

    load_easyocr()

    # pool = Pool(3)

    # pool.apply_async(read_thread,  args=[bbox])
    # pool.apply_async(say_thread,  args=[])

    # pool.close()    #关闭进程池，关闭后pool不能再添加新的请求
    # pool.join()     #等待pool中所有子进程执行完成，必须放在close语句之后

    rt = threading.Thread(target=read_thread, args=[], daemon=True)
    st = threading.Thread(target=say_thread, args=[], daemon=True)

    rt.start()
    st.start()

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        pass
