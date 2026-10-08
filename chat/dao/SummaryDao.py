from common.LoadPggresql import pool

def query_summary_memory(historyId: int):
    with pool.connection() as con:
        with con.cursor() as cursor:
            sql = "select summary from rag_summary where history_id= %s"
            cursor.execute(sql, [historyId])
            rs = cursor.fetchone()
            if rs:
                return rs[0]
            else:
                return ""

def save_summary_memory(historyId: int,summary: list):
    try:
        with pool.connection() as con:
            with con.cursor() as cursor:
                sql = "insert into rag_summary(history_id, summary, create_time, update_time)VALUES(%s, %s, NOW(), NOW()) on conflict(history_id) do UPDATE set summary=EXCLUDED.summary, update_time = NOW();"
                cursor.execute(sql,[historyId,summary])
                con.commit()
                return cursor.rowcount
    except Exception as e:
        print(f"摘要存储出现异常：{e}")
        return -1


def delete_summary_memory(historyId: int):
    rs = query_summary_memory(historyId)
    if not rs:
        return 1
    try:
        with pool.connection() as con:
            with con.cursor() as cursor:
                sql = "delete from rag_summary where history_id= %s"
                cursor.execute(sql, [historyId])
                con.commit()
                return 1
    except Exception as e:
        print(f"摘要删除出现异常：{e}")
        return -1