"""报告: htmltestreport"""
# 1. 导包
import os

from htmltestreport import HTMLTestReport
import unittest
# 2. 组合测试套件
# 默认为 pattern="test*.py, 脚本文件以 test 开头就不需要执行, 否则需要自己指定
from config import DIR_PATH

suite = unittest.defaultTestLoader.discover("./script")
# 3. 执行测试套件
# 指定测试报告存储目录
report_path=DIR_PATH+os.sep+"report"+os.sep+"p2p.html"
HTMLTestReport(report_path,title="黑马理财系统接口自动化test",description="python+requests+parameterized+beautifulSoup+pymysql").run(suite)