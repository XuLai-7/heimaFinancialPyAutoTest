# api中任意一个 文件代码被使用, __init__ 中的代码会自动执行
# 初始化 日志器对象
from util.get_log import GetLog

# 自动执行
log = GetLog.get_log()