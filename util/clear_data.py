# 清除方法
from util.conn_sql import conn_mysql


def clear_data():
    sql1 = """
       delete i.* from mb_member_info i INNER JOIN mb_member m on i.member_id=m.id where m.phone in ("13600001111","13600001112","13600001113","13600001114")
       """
    conn_mysql(sql1)
    sql2 = """
       delete l.* from mb_member_login_log l INNER JOIN mb_member m on l.member_id=m.id where m.phone in ("13600001111","13600001112","13600001113","13600001114")
       """
    conn_mysql(sql2)
    sql3 = """
       delete from mb_member_register_log where phone in ("13600001111","13600001112","13600001113","13600001114")
       """
    conn_mysql(sql3)
    sql4 = """
       delete from mb_member where phone in ("13600001111","13600001112","13600001113","13600001114")
       """
    conn_mysql(sql4)
