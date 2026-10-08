from fastapi import FastAPI
from common.LoadModel import LoadModel
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.load_model = LoadModel()
    print("成功加载模型")
    yield
    del app.state.load_model
    print("关闭模型对象")
app = FastAPI(lifespan=lifespan)

# 跨域配置
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8888"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

from chat.contorller.ChatContorller import chat_router
app.include_router(chat_router,prefix="/chat",tags=["chat"])

from chat.contorller.HistoryContorller import history_router
app.include_router(history_router,prefix="/history",tags=["history"])

from users.contorller.UsersContorller import users_router
app.include_router(users_router,prefix="/users",tags=["users"])


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)