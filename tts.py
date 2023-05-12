from util import log_factory
import pyttsx3
import threading
import subprocess

class TTSThread(threading.Thread):

    def __init__(self, queue, vits=False) -> None:
        super().__init__()
        self.queue = queue

        self.thread = None
        self.vits = vits
        
        pass
    
    def add_to_queue(self, txt):
        self.queue.put(txt)

    def run(self):

        log = log_factory.getTTSLog()

        log.info("# 开启朗读进程")

        while (True):

            r = self.queue.get()
            log.info('朗读：%s' % r)

            try:

                if self.vits:
                    self.say_vits(r)
                else:
                    self.say(r)
                # paimon_speeker.say(r)
                # log.info('朗读结束')
            except Exception as e:
                log.error(e)

    def say(self, text, timeout=10):
        engine = pyttsx3.init()
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate+50)

        engine.say(text)

        engine.runAndWait()

    def say_vits(self, text):

        # 运行另外一个Python脚本，并传递参数
        result = subprocess.run(['python', 'test.py', text],
                            cwd="./model/VITS-Paimon", capture_output=True)