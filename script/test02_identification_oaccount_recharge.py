import unittest

import requests
from parameterized import parameterized

from api import log
from api.api_identification_oaccount import IdentificationOaccount

# 三方开户, 三方充值: 需要从响应数据中提取input标签的name属性和value属性值.
from util.paraser_html import paraser_html
from util.read_json import read_json


class TestIdentificationOaccount(unittest.TestCase):
    # 初始化
    def setUp(self) -> None:
        # 1.获取session
        self.session = requests.session()
        # 2.获取IdentificationOaccount实例对象, 封装的接口方法都在这个类的实例对象中
        self.approve = IdentificationOaccount(self.session)
        # 调用登录成功
        self.approve.api_login()

    # 结束
    def tearDown(self) -> None:
        # 关闭session
        self.session.close()

    # 认证接口 测试
    def test01_identification(self):
        try:
            resp = self.approve.api_identification()
            print(resp.json())
            # 断言
            log.info("接口执行结果为:{}".format(resp.text))
            self.assertIn("提交成功", resp.text)
            log.info("断言通过")
        except Exception as e:
            # 日志
            log.error("断言错误! 原因:{}".format(e))
            # 抛异常
            raise

    # 查询认证状态接口 测试
    def test02_get_identification_status(self):
        try:
            resp = self.approve.api_get_identification_status()
            print(resp.json())
            # 断言
            log.info("接口执行结果为:{}".format(resp.text))
            self.assertIn("华", resp.text)
            log.info("断言通过")
        except Exception as e:
            # 日志
            log.error("断言错误! 原因:{}".format(e))
            # 抛异常
            raise

    # 后台开户接口 测试
    def test03_trust(self):
        try:
            resp = self.approve.api_trust()
            # resp.text 会转为 unicode 编码, 使用 resp.json() 数据格式正常
            log.info("接口执行结果为:{}".format(resp.json()))
            # print(resp.json())
            self.assertIn("form", resp.text)
            log.info("断言通过")
            # 三方开户
            # 三方请求没有 url , 没有data, 封装没有意义,就在脚本层编写了
            result = paraser_html(resp)
            print(result)
            r = self.session.post(url=result[0], data=result[1])
            log.info("接口执行结果为:{}".format(r.text))
            self.assertIn("OK", r.text)

        except Exception as e:
            # 日志
            log.error("断言错误! 原因:{}".format(e))
            # 抛异常
            raise

    # 获取充值图片验证码接口 测试
    @parameterized.expand(read_json("approve_trust.json", "img_code"))
    def test04_img_code(self, random, expect_result):
        try:
            resp = self.approve.api_img_code(random)
            # 返回的是图片,二进制数据
            log.info("接口执行结果为:{}".format(resp.status_code))
            # int 不能进行迭代 In 不行
            self.assertEqual(expect_result, resp.status_code)
            log.info("断言通过")
        except Exception as e:
            # 日志
            log.error("断言错误! 原因:{}".format(e))
            # 抛异常
            raise

    # 充值接口 测试
    @parameterized.expand(read_json("approve_trust.json", "recharge"))
    def test05_recharge(self, valicode, expect_result):
        result = None
        try:
            # 调用图片验证码, 获取 cookie
            self.approve.api_img_code(1231123)
            resp = self.approve.api_recharge(valicode)
            print(resp.json())
            # 返回的是图片,二进制数据
            log.info("接口执行结果为:{}".format(resp.json()))
            # int 不能进行迭代 In 不行
            # 三方充值
            # 三方请求没有 url , 没有data, 封装没有意义,就在脚本层编写了
            # 验证码错误, 不会返回 form , 解析 html 提取 form 数据就会报错
            # 充值需要判断验证码不同, 执行步骤和结果不同
            if valicode == 8888:
                # 验证码为 8888, 提取 form 数据,三方充值,断言 OK.
                result = paraser_html(resp)
                print(result)
                r = self.session.post(url=result[0], data=result[1])
                log.info("接口执行结果为:{}".format(r.text))
                self.assertIn(expect_result, r.text)
            else:
                # 验证码不是 8888, 直接断言 验证码错误
                self.assertIn(expect_result, resp.text)

        except Exception as e:
            # 日志
            log.error("断言错误! 原因:{}".format(e))
            # 抛异常
            raise
