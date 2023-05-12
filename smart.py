# 定义 Producer 类
import threading
import hashlib
# 文本相似度
from difflib import SequenceMatcher
from sentence_transformers import SentenceTransformer as SBert
from sentence_transformers.util import cos_sim
import numpy as np

from util import log_factory
from util.timing import timing


sentences1 = np.array([''])
RATIO = 0.6

class SmartThread(threading.Thread):

    def __init__(self, in_queue, out_queue):
        super().__init__()
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.logger = log_factory.getSmartLog()
        self.model = SBert('./model/paraphrase-multilingual-MiniLM-L12-v2')

    def run(self):
        while True:
            text = self.in_queue.get()
            timing(self.samrt_say, text, "智能处理", self.logger)

    def samrt_say(self, text):
        
        global sentences1
        global RATIO

        if not isinstance(text, list):
            self.logger.info(type(text) + ', 不支持的类型')
            return

        text = [v for v in text if self.is_contain_chinese(v) and not (
            self.find(v, ['ID', 'UID', 'Lv', 'LV', 'Enter',
                'E', 'Q', 'R', '保存配置', '快速列队', '活动']) or self.is_number(v)
        )]

        sentences2 = np.array([','.join(text)])

        # LOG.info("sentences1: %s" % sentences1)
        # LOG.info("sentences2: %s" % sentences2)

        # ratio = SequenceMatcher(None, tmp_text['1'], text).ratio()

        # Compute embedding for both lists
        embeddings1 = self.model.encode(sentences1)
        embeddings2 = self.model.encode(sentences2)

        # Compute cosine-similarits
        cosine_scores = cos_sim(embeddings1, embeddings2)
        # cosine_scores_diag = cosine_scores.diag()
        ratio = cosine_scores.mean().float()

        # LOG.info('相似度: %s' % (str(cosine_scores)))
        # LOG.info('相似度: %s' % (str(cosine_scores_diag)))
        # LOG.info('model相似度: %s' % (str(ratio)))
        # LOG.info('ratio相似度:' + str(ratio))
        # LOG.info('相似度:' + str(cosine_scores.mean()))
        # for i in range(len(text)):
        # LOG.info("{} \t\t {} \t\t Score: {:.4f}".format('1', '2', cosine_scores[i][i]))

        # difflib 相似度
        s = SequenceMatcher(None, sentences1[0], sentences2[0])
        ratio2 = s.ratio()
        # LOG.info('difflib相似度: %s' % (str(ratio2)))

        if (ratio > RATIO and ratio2 > RATIO):
            return

        # LOG.info("刷新缓存sentences1...")
        sentences1 = sentences2

        for t in text:
            if "UID" in t:
                continue
            if "ID" in t:
                continue

            self.logger.info("添加到朗读队列: %s" % t)
            self.out_queue.put(t)

        
    def md5(self, data):
        return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()


    def find(self, s, c):

        if isinstance(c, list):
            for v in c:
                if v in s:
                    return True
            return False
        else:
            return c in s

    # 判断是否为数字
    def is_number(self, s):
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


    def is_contain_chinese(self, check_str):
        """
        判断字符串中是否包含中文
        :param check_str: {str} 需要检测的字符串
        :return: {bool} 包含返回True， 不包含返回False
        """
        for ch in check_str:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False