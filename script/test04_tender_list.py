import unittest

import requests

from api import log
from api.api_identification_oaccount import IdentificationOaccount
from api.api_register_login import ApiRegisterLogin
from api.api_tender import ApiTender
from util.paraser_html import paraser_html


class TestTenderList(unittest.TestCase):
    # 初始化
    def setUp(self) -> None:
        # 获取session对象, 自动管理 接口请求中的cookie数据.
        self.session = requests.session()
        self.reg = ApiRegisterLogin(self.session)
        self.approve = IdentificationOaccount(self.session)
        self.tender = ApiTender(self.session)

    # 结束
    def tearDown(self) -> None:
        self.session.close()

    # 测试函数
    def test01_tender_list(self):
        # 根据Jemter中投资业务的接口顺序
        phone = 13600001111
        password = "test123"
        img_code = 8888
        phone_code = 666666
        self.reg.api_img_code(0.123)
        self.reg.api_phone_code(phone, img_code)
        self.reg.api_register(phone, password, img_code, phone_code)
        self.reg.api_login(phone, password)
        self.approve.api_identification()
        resp = self.approve.api_trust()
        result = paraser_html(resp)
        resp =self.session.post(url=result[0], data=result[1])
        log.info("接口执行结果为:{}".format(resp.text))

        self.reg.api_img_code(0.123)
        resp = self.approve.api_recharge(img_code)
        result = paraser_html(resp)
        resp =self.session.post(url=result[0], data=result[1])
        log.info("接口执行结果为:{}".format(resp.text))

        resp = self.tender.api_tender(100)
        result = paraser_html(resp)
        resp = self.session.post(url=result[0], data=result[1])
        log.info("接口执行结果为:{}".format(resp.text))
        self.assertIn("OK", resp.text)
