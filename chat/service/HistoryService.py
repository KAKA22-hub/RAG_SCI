from chat.dao import HistoryDao
from chat.entity.SaveResultEntity import SaveResultEntity
from chat.dao import SummaryDao

def query_history_menu(usersId):
    rs = HistoryDao.query_history_by_usersid(usersId)
    data = []
    for item in rs:
        data.append({
            "historyId":item['history_id'],
            "question":item['question'],
            "answer":item['answer'],
            "createTime":item['create_time'].strftime('%Y-%m-%d %H:%M:%S'),
        })
    return {
        "code":200,
        "msg":"查询成功",
        "data":data
    }

def query_history_list(historyId):
    rs = HistoryDao.query_history_by_historyid(historyId)
    data = []
    for item in rs:
        data.append({
            "role":"user",
            "content":item['question']
        })
        data.append({
            "role":"system",
            "content":item['answer']
        })
    return {
        "code":200,
        "msg":"查询成功",
        "data":data
    }

def save_chat_history(saveResultEntity):
    rs = HistoryDao.save_chat_result(saveResultEntity)
    if rs > 0:
        return {
            "code":200,
            "msg":"保存成功",
            "data":rs
        }
    else:
        return {
            "code":500,
            "msg":"保存失败",
            "data":None
        }

def delete_chat_history(historyId):
    rs = HistoryDao.delete_history_by_historyid(historyId)
    rs_s = SummaryDao.delete_summary_memory(historyId)
    if rs > 0 and rs_s > 0:
        return {
            "code":200,
            "msg":"删除成功",
            "data":None
        }
    else:
        return {
            "code":500,
            "msg":"删除失败",
            "data":None
        }

if __name__ == '__main__':
    # entity = SaveResultEntity(
    #     usersId=1,
    #     question="555",
    #     answer="666",
    #     parentId=3
    # )
    # rs = save_chat_history(entity)
    # print(rs)
    RS = query_history_menu(1)
    print(RS)
    RS = query_history_list(1)
    print(RS)