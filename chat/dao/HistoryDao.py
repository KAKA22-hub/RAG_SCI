from common.LoadDataMysql import LoadMysql
from chat.entity.SaveResultEntity import SaveResultEntity

def query_history_by_usersid(usersId):
    mysql = LoadMysql().conn
    cursor = mysql.cursor()
    sql = "select * from `history` where users_id = %s and parent_id=0"
    cursor.execute(sql, [usersId])
    result = cursor.fetchall()
    LoadMysql().close_conn(cursor, mysql)
    return result

def query_history_by_historyid(historyId):
    mysql = LoadMysql().conn
    cursor = mysql.cursor()
    sql = "select * from `history` where history_id = %s or parent_id=%s order by history_id asc;"
    cursor.execute(sql, [historyId, historyId])
    result = cursor.fetchall()
    LoadMysql().close_conn(cursor, mysql)
    return result

def save_chat_result(SaveResultEntity):
    try:
        mysql = LoadMysql().conn
        cursor = mysql.cursor()
        sql = "insert into `history` values(null,%s,%s,%s,%s,now())"
        cursor.execute(sql,[
            SaveResultEntity.usersId,
            SaveResultEntity.question,
            SaveResultEntity.answer,
            SaveResultEntity.parentId
        ])
        mysql.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"存储历史记录出现异常：{e}")
        mysql.rollback()
        return -1
    finally:
        LoadMysql().close_conn(cursor, mysql)

def delete_history_by_historyid(historyId):
    try:
        mysql = LoadMysql().conn
        cursor = mysql.cursor()
        sql = "delete from `history` where history_id = %s or parent_id = %s"
        rs = cursor.execute(sql, [historyId, historyId])
        mysql.commit()
        return rs
    except Exception as e:
        print(f"删除历史对话出现异常：{e}")
        mysql.rollback()
        return -1
    finally:
        LoadMysql().close_conn(cursor, mysql)
