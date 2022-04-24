import unittest
from time import sleep

import requests
from parameterized import parameterized

from api import log
from api.api_register_login import ApiRegisterLogin
from util.clear_data import clear_data
from util.read_json import read_json
import logging


class TestRegisterLogin(unittest.TestCase):
    # 清除测试数据
    @classmethod
    def setUpClass(cls) -> None:
        # 清除数据
        # 类方法调用, test01 跑之前,先清一次.
        # 每次先清再注册, 就都可以成功了
        clear_data()

    # 初始化
    def setUp(self):
        # 获取session对象
        self.session = requests.session()
        log.info("正在初始化session对象:{}".format(self.session))
        # 获取 ApiRegisterLogin 实例
        self.reg = ApiRegisterLogin(self.session)

    # 结束
    def tearDown(self):
        # 关闭session 对象
        log.info("正在关闭session对象:{}".format(self.session))
        self.session.close()

    # 测试方法
    # 测试api中封装的方法 api 中封装哪些方法, 这里就测试哪些方法
    # 1. 封装 获取图片验证码接口 test
    @parameterized.expand(read_json("register_login.json", "img_code"))
    def test01_img_code(self, random, expect_result):
        # 断言可能会出错, 要用 异常包裹
        try:
            resp = self.reg.api_img_code(random)
            log.info("执行图片验证码响应状态码为:{}".format(resp.status_code))
            # 取状态码: status_code
            self.assertEqual(expect_result, resp.status_code)
            log.info("执行图片验证码断言通过")
        except Exception as e:
            # 日志
            log.error("断言失败, 原因{}".format(e))

            # 抛异常 ,出错不抛异常, 被捕获,不抛异常,就通过了, 抛异常, 就不通过 就对了
            # 捕获异常的目的: 将异常记录到日志文件,过滤, 然后再抛出异常
            raise

    # 2. 封装 获取短信验证码接口 test
    @parameterized.expand(read_json("register_login.json", "phone_code"))
    def test02_phone_code(self, phone, imgVerifyCode, expect_result):
        try:
            # 1.调用 获取图片验证码接口 -- 目的: 让 session 对象 自动记录 cookie
            self.reg.api_img_code(0.123)
            resp = self.reg.api_phone_code(phone, imgVerifyCode)
            log.info("执行短信验证码响应内容{}".format(resp.text))
            self.assertIn(expect_result, resp.text)
            log.info("执行断言通过")

        except Exception as e:
            # 日志
            log.error("断言失败, 原因{}".format(e))
            # 抛异常 ,出错不抛异常, 被捕获,不抛异常,就通过了, 抛异常, 就不通过 就对了
            # 捕获异常的目的: 将异常记录到日志文件,过滤, 然后再抛出异常
            raise

    # 3. 封装 注册接口 test
    @parameterized.expand(read_json("register_login.json", "register"))
    def test03_register(self, phone, password, verifycode, phone_code, expect_result):
        try:
            # 1.调用 获取图片验证码接口 -- 目的: 让 session 对象 自动记录 cookie
            self.reg.api_img_code(0.123)
            # 日志文件显示 注册接口验证码过期或无效，请重新获取, 故查看 图片验证码和短信验证码请求, 发现, 图片验证码没有问题, 短信验证码的请求参数写错,应为 手机号加图片验证码, 写成了 手机号加密码, 故提示验证码错误, 导致注册失败,导致登录锁定接口没有这个注册成功的用户,故日志文件断言结果为用户不存在,导致无法登录,无法实现解锁功能,断言出错
            self.reg.api_phone_code(phone, verifycode)
            resp = self.reg.api_register(phone, password, verifycode, phone_code)
            log.info("执行注册响应内容为:{}".format(resp.text))
            # resp.text 更方便
            self.assertIn(expect_result, resp.text)
            log.info("执行断言通过")

        except Exception as e:
            # 日志
            log.error("断言失败, 原因{}".format(e))

            # 抛异常 ,出错不抛异常, 被捕获,不抛异常,就通过了, 抛异常, 就不通过 就对了
            # 捕获异常的目的: 将异常记录到日志文件,过滤, 然后再抛出异常
            raise

    # 4. 封装 登录接口 test
    @parameterized.expand(read_json("register_login.json", "login"))
    def test04_login(self, keywords, password, expect_result):
        try:
            i = 1
            resp = None
            if "error" in password:
                while i <= 3:
                    resp = self.reg.api_login(keywords, password)
                    log.info("执行登录响应内容为:{}".format(resp.text))
                    i += 1
                # 断言锁定
                self.assertIn("锁定", resp.text)
                log.info("执行断言通过")

                # 暂停60秒
                sleep(60)
                resp = self.reg.api_login(keywords, "test123")
                log.info("执行登录响应内容为:{}".format(resp.text))

                # 断言登录成功
                self.assertIn(expect_result, resp.text)
                log.info("执行断言通过")

            else:
                resp = self.reg.api_login(keywords, password)
                log.info("执行登录响应内容为:{}".format(resp.text))

                self.assertIn(expect_result, resp.text)
                log.info("执行断言通过")

        except Exception as e:
            # 日志
            log.error("断言失败, 原因{}".format(e))

            # 抛异常 ,出错不抛异常, 被捕获,不抛异常,就通过了, 抛异常, 就不通过 就对了
            # 捕获异常的目的: 将异常记录到日志文件,过滤, 然后再抛出异常
            raise

    # 5. 封装 查询登录状态接口 test
    @parameterized.expand(read_json("register_login.json", "login_status"))
    def test05_login_status(self, status, expect_result):
        try:
            # 调用登录接口
            if status == "已登录":
                self.reg.api_login(13600001111, "test123")
                # 调用查询登录状态接口
                resp = self.reg.api_login_status()
                log.info("执行查询登录状态响应内容为:{}".format(resp.text))

                self.assertIn(expect_result, resp.text)
                log.info("执行断言通过")

            else:
                resp = self.reg.api_login_status()
                log.info("执行查询登录状态响应内容为:{}".format(resp.text))

                self.assertIn(expect_result, resp.text)
                log.info("执行断言通过")

        except Exception as e:
            # 日志
            log.error("断言失败, 原因{}".format(e))

            # 抛异常 ,出错不抛异常, 被捕获,不抛异常,就通过了, 抛异常, 就不通过 就对了
            # 捕获异常的目的: 将异常记录错误信息记录到日志文件, 然后必须再抛出异常
            raise
