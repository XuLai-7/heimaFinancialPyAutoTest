import requests

from api import log
from config import HOST


class ApiRegisterLogin:
    # 模块中有几个接口,就封装几个方法
    # 最多再加一个初始化方法
    # 初始化方法 公共的方法和变量
    def __init__(self, session):
        # 获取 session 对象
        # 下面方法中的接口请求都需要用到 session 对象
        self.session = session
        # 封装接口url
        # url 并不是公共相同的,可以定义在每个不同方法内部
        # 写成私有的,就当前模块文件需要使用 url, 其他文件看不见这个url...,体验比较好
        self.__url_img_code = HOST + "/common/public/verifycode1/{}"
        self.__url_phone_code = HOST + "/member/public/sendSms"
        self.__url_register = HOST + "/member/public/reg"
        self.__url_login = HOST + "/member/public/login"
        self.__url_login_status = HOST + "/member/public/islogin"

    # 1. 封装 获取图片验证码接口
    def api_img_code(self, radom):
        log.info("正在调用验证码接口,请求方法:{},请求url:{}".format("get", self.__url_img_code.format(radom)))
        # 调用 GET 方法, 返回响应对象
        return self.session.get(url=self.__url_img_code.format(radom))

    # 2. 封装 获取短信验证码接口
    def api_phone_code(self, phone, imgVerifyCode):
        # 1. 定义请求参数 2. 调用请求方法
        data = {"phone": phone, "imgVerifyCode": imgVerifyCode, "type": "reg"}
        # 使用 session 来处理请求, 不用管 处理 cookie, 自动管理
        # 请求头也不需要, data 默认是 form. 默认就是表单数据, json 数据.
        log.info("正在调用短信验证码接口,请求方法:{},请求url:{}, 请求参数:{}".format("post", self.__url_phone_code, data))
        return self.session.post(url=self.__url_phone_code, data=data)

    # 3. 封装 注册接口
    def api_register(self, phone, password, verifycode, phone_code):
        data = {"phone": phone, "password": password, "verifycode": verifycode,
                "phone_code": phone_code, "dy_server": "on"
                }
        log.info("正在调用注册接口,请求方法:{},请求url:{}, 请求参数:{}".format("post", self.__url_register, data))
        return self.session.post(url=self.__url_register, data=data)

    # 4. 封装 登录接口
    def api_login(self, keywords, password):
        data = {"keywords": keywords, "password": password}
        log.info("正在调用登录接口,请求方法:{},请求url:{}, 请求参数:{}".format("post", self.__url_login, data))
        return self.session.post(url=self.__url_login, data=data)

    # 5. 封装 查询登录状态接口
    def api_login_status(self):
        log.info("正在调用查询登录状态接口,请求方法:{},请求url:{}".format("post", self.__url_login_status))
        return self.session.post(url=self.__url_login_status)
