import logging
import os

LOG_DIR = "logs"

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_MAP = {}


def createLog(name, logfile):

    # 第一步，创建一个logger

    LOG = logging.getLogger(name)

    LOG.setLevel(logging.INFO)  # Log等级总开关

    # 第二步，创建一个handler，用于写入日志文件
    logfile = logfile

    fh = logging.FileHandler(
        logfile, mode='a', encoding='utf8')  # open的打开模式这里可以进行参考

    fh.setLevel(logging.INFO)  # 输出到file的log等级的开关

    # 第三步，再创建一个handler，用于输出到控制台

    ch = logging.StreamHandler()

    ch.setLevel(logging.INFO)  # 输出到console的log等级的开关

    # 第四步，定义handler的输出格式
    formatter = logging.Formatter(
        "%(asctime)s - %(name)-8s - %(filename)-8s[line:%(lineno)3d] - %(levelname)s: %(message)s")

    fh.setFormatter(formatter)

    ch.setFormatter(formatter)

    # 第五步，将logger添加到handler里面

    LOG.addHandler(fh)

    LOG.addHandler(ch)

    return LOG


def getLog():

    name = "派蒙语音"
    logfile = LOG_DIR + "/main.log"

    if LOG_MAP.get(name):
        return LOG_MAP.get(name)

    LOG = createLog(name, logfile)
    LOG_MAP[name] = LOG

    return LOG


def getTTSLog():

    name = "派蒙语音-朗读"
    logfile =  LOG_DIR + "/tts.log"

    if LOG_MAP.get(name):
        return LOG_MAP.get(name)

    LOG = createLog(name, logfile)
    LOG_MAP[name] = LOG

    return LOG


def getReadLog():

    name = "派蒙语音-识图"
    logfile = LOG_DIR + '/ocr.log'

    if LOG_MAP.get(name):
        return LOG_MAP.get(name)

    LOG = createLog(name, logfile)
    LOG_MAP[name] = LOG

    return LOG


def getSmartLog():

    name = "派蒙语音-智能"
    logfile = LOG_DIR + '/smart.log'

    if LOG_MAP.get(name):
        return LOG_MAP.get(name)

    LOG = createLog(name, logfile)
    LOG_MAP[name] = LOG

    return LOG
