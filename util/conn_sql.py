# 连接数据库工具
import pymysql

from api import log

"""
    查询语句: 返回所有的结果
    非查询语句: DML 语句, 返回受影响的行数
"""


def conn_mysql(sql):
    conn = None
    cursor = None
    try:
        # 获取连接对象
        # autocommit 默认false, 设为true, 自动提交事务
        conn = pymysql.connect(host="121.43.169.97", user="root", password="Itcast_p2p_20191228",
                               database="czbk_member", port=3306, charset="utf8",
                               autocommit=True)
        # 获取游标对象
        cursor = conn.cursor()
        # 执行sql语句
        cursor.execute(sql)
        # 判断sql语句是否为查询
        if sql.split()[0].lower() == "select":
            # 返回 所有的结果
            return cursor.fetchall()
        else:
            # 返回 受影响的行数
            return "受影响的行数为{}".format(cursor.rowcount)

    except Exception as e:
        # sql语句执行错误,写入日志
        log.error(e)
        # 抛出异常
        raise
    finally:
        # 关闭游标
        cursor.close()
        # 关闭连接
        conn.close()


if __name__ == '__main__':
    sql = "select * from mb_member"
    sql2 = "delete from mb_member where phone = '18916910061'"
    print(conn_mysql(sql2))
