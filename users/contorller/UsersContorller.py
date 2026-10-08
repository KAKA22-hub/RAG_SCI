from fastapi import APIRouter
from starlette.responses import StreamingResponse
from users.service import UsersService
import json
from users.entity.RegistrationEntity import RegisterEntity
from common import Jwtutils

users_router = APIRouter()

@users_router.get("/sendCaptcha")
def send_captcha(email: str):
    return UsersService.send_code(email)

@users_router.get("/login")
def login_by_captcha(email: str, captcha: str):
    # return UsersService.login(email, captcha)
    result = UsersService.login(email, captcha)
    if result["code"] != 200:
        return result
    data = result["data"]
    token = Jwtutils.create_token({
        "usersId": data["user_id"],
        "nickname": data["nickname"],
        "email": data["email"],
        "email_password": data["email_password"],
        "rolesId": data['roles_id'],
    })
    return {
        "code": 200,
        "msg": "登录成功",
        "data": {"token": token}
    }

@users_router.post("/regist")
def regist(RegisterEntity: RegisterEntity):
    return UsersService.register(RegisterEntity)

@ users_router.post("/login")
def login_by_password(email: str, password: str):
    result = UsersService.password_login(email, password)
    if result["code"] != 200:
        return result
    data = result["data"]
    token = Jwtutils.create_token({
        "usersId": data["user_id"],
        "nickname": data["nickname"],
        "email": data["email"],
        "email_password": data["email_password"],
        "rolesId": data['roles_id'],
    })
    return {
        "code": 200,
        "msg": "登录成功",
        "data": {"token": token}
    }