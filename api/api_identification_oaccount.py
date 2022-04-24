from api import log
from config import HOST


class IdentificationOaccount:

    def __init__(self, session):
        # 初始化session,自动管理cookie,解决cookie的问题
        # 存储以下方法公共的变量和方法
        self.session = session

    # 测试函数
    # 4. 封装 登录接口
    # 给了默认参数,再传参会覆盖默认参数
    def api_login(self, keywords="13600001111", password="test123"):
        url = HOST + "/member/public/login"
        # 定义请求参数
        data = {"keywords": keywords, "password": password}
        log.info("正在调用登录接口,请求方法:{},请求url:{}, 请求参数:{}".format("post", url, data))
        return self.session.post(url=url, data=data)

    # 认证接口 封装
    def api_identification(self):
        url = HOST + "/member/realname/approverealname"
        # 认证接口并没有要求测试多个, 数据写死,不用参数化
        data = {"realname": "华仔", "card_id": "350102199003072237"}
        # 调用请求方法
        # 请求头参数: multipart/form-data　多消息体，一次上传多种数据类型的参数
        # 传data默认是form
        # data+files 会自动识别为 multipart/form-data　实现多消息体类型, 这里files中传的参数没有实际意义
        # 正常上传文件用 files
        return self.session.post(url=url, data=data, files={"x": "y"})

    # 查询认证状态接口 封装
    def api_get_identification_status(self):
        url = HOST + "/member/member/getapprove"
        return self.session.post(url=url)

    # 后台开户接口 封装
    def api_trust(self):
        url = HOST + "/trust/trust/register"
        return self.session.post(url=url)

    # 获取图片验证码接口 封装
    def api_img_code(self, random):
        # 调用 GET 方法, 返回响应对象
        url = HOST + "/common/public/verifycode/{}".format(random)
        return self.session.get(url=url)

    # 充值接口封装
    def api_recharge(self, valicode):
        url = HOST + "/trust/trust/recharge"
        data = {"paymentType": "chinapnrTrust",
                "amount": 1000,
                "formStr": "reForm",
                "valicode": valicode
                }
        return self.session.post(url=url, data=data)
