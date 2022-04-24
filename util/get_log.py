# 日志工具
import logging.handlers
import os

from config import DIR_PATH


class GetLog:
    log = None

    @classmethod
    def get_log(cls):
        cls.log = None
        if cls.log is None:
            # 获取日志器
            cls.log = logging.getLogger()
            # 设置日志级别 info
            cls.log.setLevel(logging.INFO)
            filepath = DIR_PATH + os.sep + "log" + os.sep + "p2p.log"
            # 获取处理器 TimedRotatingFileHandler: 日志保存到文件且根据时间去分割
            # midnight: 一天一夜
            tf = logging.handlers.TimedRotatingFileHandler(filename=filepath,
                                                           when="midnight",
                                                           interval=1,
                                                           backupCount=3,
                                                           encoding="utf-8")
            # 获取格式器
            # 时间 级别 模块名称 函数名称 行号 日志消息
            fmt = "%(asctime)s %(levelname)s [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s"
            # 获取格式器
            fm = logging.Formatter(fmt)
            # 将格式器添加到处理器中
            tf.setFormatter(fm)
            # 将处理器添加到日志器中
            cls.log.addHandler(tf)
        # 返回日志器
        return cls.log


if __name__ == '__main__':
    log = GetLog.get_log()
    # 信息级别测试
    log.info("test")
