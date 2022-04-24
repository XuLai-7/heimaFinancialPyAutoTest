import logging

# 设置日志级别
logging.basicConfig(level=logging.DEBUG, filename="../log/p2p.log")

# 调用日志
logging.debug("调试信息")
logging.info("信息级别")
logging.warning("警告级别")
logging.error("断言错误")
logging.critical("严重错误")
