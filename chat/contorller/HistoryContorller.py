from fastapi import APIRouter,Depends
from chat.service import HistoryService
from chat.entity.SaveResultEntity import SaveResultEntity
from common.Jwtutils import get_current_user

history_router = APIRouter()

@history_router.get("/queryHistoryMenu/{usersId}")
def quert_history_menu(usersId: str,user = Depends(get_current_user)):
    return HistoryService.query_history_menu(int(usersId))

@history_router.get("/queryHistoryList/{historyId}")
def query_history_list(historyId: str):
    return HistoryService.query_history_list(int(historyId))

@history_router.post("/saveChatResult")
def save_chat_result(saveResultEntity: SaveResultEntity):
    return HistoryService.save_chat_history(saveResultEntity)

@history_router.post("/deleteChatHistory/{historyId}")
def delete_chat_history(historyId: str):
    return HistoryService.delete_chat_history(int(historyId))