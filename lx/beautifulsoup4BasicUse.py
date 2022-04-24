# 导包
from bs4 import BeautifulSoup

html = """
    <html>
        <head>
            <title>程序员</title>
        </head>
        <body>
            <p id="test01">软件</p>
            <p id="test02">2022年</p>
            <a href="/api.html">接口</a>
            <a href="/web.html">Web自动化</a>
            <a href="/app.html">APP自动化</a>
        </body>
    </html>
"""
# 获取bs对象 html.parser 表示解析的是 html 格式
bs = BeautifulSoup(html, "html.parser")
# 调用方法 重点: 1.查找所有标签 bs.find_all("标签名") 元素的集合, 2.查找属性 元素.get("属性名")

for a in bs.find_all("a"):
    print(a.get("href"))
# 扩展其他方法
# 获取单个元素 bs.标签名 默认返回第一个
print(bs.a)
# 获取文本
print(bs.a.string)
# 获取属性
print(bs.a.get("href"))
# 获取标签名
print(bs.a.name)