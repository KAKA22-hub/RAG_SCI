from common.LoadDataMysql import LoadMysql
from users.entity.RegistrationEntity import RegisterEntity
from users.entity.UpdateEntity import UpdateEntity

def query_usersinfo_by_email(email):
    mysql = LoadMysql().load_mysql_conn()
    cursor = mysql.cursor()
    sql = "select * from `users_info` where email=%s"
    cursor.execute(sql,[email])
    result = cursor.fetchall()
    LoadMysql().close_conn(cursor,mysql)
    return result

def query_usersinfo_by_usersId(usersId):
    mysql = LoadMysql().load_mysql_conn()
    cursor = mysql.cursor()
    sql = "select * from `users_info` where users_id=%s"
    cursor.execute(sql,[usersId])
    result = cursor.fetchall()
    LoadMysql().close_conn(cursor,mysql)
    return result

def save_usersinfo_by_email(RegisterEntity):
    try:
        mysql = LoadMysql().load_mysql_conn()
        cursor = mysql.cursor()
        sql = "insert into `users_info` values(null,%s,%s,%s,%s,%s)"
        cursor.execute(sql,[
            RegisterEntity.email,
            RegisterEntity.nickname,
            RegisterEntity.password,
            RegisterEntity.roles_id,
            RegisterEntity.email_password,
        ])
        mysql.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"注册出现异常：{e}")
        mysql.rollback()
        return -1
    finally:
        LoadMysql().close_conn(cursor,mysql)

def update_usersinfo_by_usersId(usersId, UpdateEntity):
    try:
        mysql = LoadMysql().load_mysql_conn()
        cursor = mysql.cursor()
        sql = "update `users_info` set nickname=%s,password=%s,roles_id=%s,email_password=%s where users_id=%s"
        cursor.execute(sql,[
            UpdateEntity.nickname,
            UpdateEntity.password,
            UpdateEntity.roles_id,
            UpdateEntity.email_password,
            usersId
        ])
        mysql.commit()
        return cursor.rowcount
    except Exception as e:
        print(f"更新出现异常：{e}")
        mysql.rollback()
        return -1
    finally:
        LoadMysql().close_conn(cursor, mysql)

if __name__ == '__main__':
    # rs = query_usersinfo_by_usersId(2)
    # print(rs)
    rs = query_usersinfo_by_email("2297474265@qq.com")
    print(rs)