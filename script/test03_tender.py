import unittest

import requests
from parameterized import parameterized

from api import log
from api.api_register_login import ApiRegisterLogin
from api.api_tender import ApiTender
from util.paraser_html import paraser_html
from util.read_json import read_json


class TestTender(unittest.TestCase):
    # 初始化
    def setUp(self) -> None:
        self.session = requests.session()
        self.tender = ApiTender(self.session)
        # 调用登录
        self.reg = ApiRegisterLogin(self.session)
        self.reg.api_login(13600001111, "test123")

    # 结束
    def tearDown(self) -> None:
        self.session.close()

    # 有密码的标没有做参数化,就不用写有密码的和有密码的标的id
    # 测试投资接口函数
    @parameterized.expand(read_json("tender.json", "tender"))
    def test01_tender(self, amount, expect_result):
        try:
            # 调用投资方法
            resp = self.tender.api_tender(amount)
            # resp.text 会有 unicode 的问题
            log.info("接口执行结果为:{}".format(resp.text))
            # 调用三方投资
            if amount == 100:
                result = paraser_html(resp)
                r = self.session.post(url=result[0], data=result[1])
                log.info("接口执行结果为:{}".format(r.text))
                self.assertIn(expect_result, r.text)
            else:
                self.assertIn(expect_result, resp.text)
        except Exception as e:
            log.error("断言错误! 原因:{}".format(e))
            raise
