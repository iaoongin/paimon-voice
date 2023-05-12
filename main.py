from smart import SmartThread
from ocr import OCRThread
from tts import TTSThread
from util import log_factory
import os
import signal
import time

from queue import Queue
from util import log_factory

def exit(a, b):
    LOG = log_factory.getLog()
    LOG.info('###########################')
    LOG.info('# ')
    LOG.info('# 退出派蒙语音')
    LOG.info('# ')
    LOG.info('###########################')
    os.kill(os.getpid(), signal.SIGILL)


def init():
    ocr_queue = Queue(100)
    tts_queue = Queue(100)

    ocr = OCRThread(queue=ocr_queue)
    tts = TTSThread(queue=tts_queue)
    # tts = TTSThread(queue=tts_queue, vits=True)
    smart = SmartThread(ocr_queue, tts_queue)

    ocr.start()
    tts.start()
    smart.start()


if __name__ == "__main__":

    LOG = log_factory.getLog()
    LOG.info('###########################')
    LOG.info('# ')
    LOG.info('# 启动派蒙语音')
    LOG.info('# ')
    LOG.info('###########################')

    signal.signal(signal.SIGINT, exit)
    signal.signal(signal.SIGTERM, exit)

    init()

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        pass
