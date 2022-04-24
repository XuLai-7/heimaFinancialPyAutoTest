from bs4 import BeautifulSoup


def paraser_html(result):
    # 提取 html
    html = result.json().get("description").get("form")
    # 获取 bs 对象
    bs = BeautifulSoup(html, "html.parser")
    # 提取 url
    url = bs.form.get("action")
    # print(url)
    # 遍历查找所有的input 标签
    inputs = bs.find_all("input")
    # 遍历进行组装  data={"version":name,"}
    data = {}
    for input in inputs:
        # 键名和键值
        data[input.get("name")] = input.get("value")
    return url, data  # 返回的是一个元组
# data 是一个 字典, 加上 url 组成元组, 返回
