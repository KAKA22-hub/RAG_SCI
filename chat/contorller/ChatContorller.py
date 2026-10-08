from fastapi import APIRouter
from starlette.responses import StreamingResponse
from chat.service import ChatService
import json
from fastapi import Query

chat_router = APIRouter()

@chat_router.get("/sci")
def stream(question: str, historyId: str, token: str = Query(None)):
    def generator():
        for item in ChatService.chat(question, historyId, token):
            yield f"data:{json.dumps({'content':str(item)})}\n\n"
        yield f"data:{json.dumps({'content':'[DONE]'})}\n\n"
    return StreamingResponse(content=generator(),media_type="text/event-stream")