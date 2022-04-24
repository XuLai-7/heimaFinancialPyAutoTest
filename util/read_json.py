"""读取json工具"""
import json
import os

from config import DIR_PATH


def read_json(filename,key):
    # 拼接读取文件的完整路径
    # os.sep 动态获取 / or  \
    file_path = DIR_PATH + os.sep + "data" + os.sep +filename
    arr = []
    with open(file_path, "r",encoding="utf-8") as f:
        for data in json.load(f).get(key):
            arr.append(tuple(data.values())[1:])
        return arr

# 列表, 字典,元组 都可以进行切片
# [1:] 切掉第一行
# arr[(),(),(),...]  切掉第一行的数据
# 列表嵌套列表 将 tuple 换成 list 即可
# [(),(),(),...] or [[],[],[],....]
if __name__ == '__main__':
    arr= read_json("register_login.json","img_code")
    print(arr)
