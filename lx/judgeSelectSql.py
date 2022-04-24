sql = "seleCT * from table"
print(type(sql))
# split 默认以空格拆分. lower 转小写, upper转大写
# 因为不知道用户传的sql语句不知道是大写还是小写,强转一下再判断.
print(sql.split()[0].lower())
