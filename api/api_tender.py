from api import log
from config import HOST


class ApiTender:
    # 初始化
    def __init__(self, session):
        self.session = session

    # 投资接口 封装
    def api_tender(self, amount, id=642):
        # 定义参数
        url = HOST + "/trust/trust/tender"
        data = {"id": id,
                "depositCertificate": -1,
                "amount": amount,
                }
        log.info("正在调用投资接口,请求方法:{},请求url:{}, 请求参数:{}".format("post", url, data))
        # 调用请求方法
        return self.session.post(url=url, data=data)
