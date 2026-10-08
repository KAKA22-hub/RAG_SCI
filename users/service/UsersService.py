from users.dao import UsersDao
from dotenv import load_dotenv
import os
from users.utils.CreateCaptchaUtil import CreateCaptcha
from common.LoadRedis import LoadRedis
from email.mime.text import MIMEText
import smtplib
from users.dao import UsersDao
from passlib.context import CryptContext

load_dotenv()
crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def send_code(email):
    result = UsersDao.query_usersinfo_by_email(email)
    if len(result) == 0:
        return {
            "code": 500,
            "msg":"邮箱不存在",
            "data":None
        }
    try:
        send_email = os.getenv("Email_USER")
        send_key = os.getenv("Email_PASSWORD")
        subject = "对话系统登录验证码"
        to = email
        code = CreateCaptcha().create_captcha()
        key = f"login:{email}"
        client = LoadRedis().redis_conn()
        client.set(key, code,ex=60)
        LoadRedis().redis_close(client)
        context = f"你的登录验证码为：{code}，有效时间60秒"
        message = MIMEText(context,"plain","utf-8")
        message["From"] = send_email
        message["To"] = to
        message["Subject"] = subject
        smtp_server = os.getenv("Email_HOST")
        smtp_port = int(os.getenv("Email_PORT"))
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        smtp.starttls()
        smtp.login(send_email, send_key)
        smtp.sendmail(message["From"], message["To"], message.as_string())
        smtp.quit()
        return {
            "code": 200,
            "msg":"验证码发送成功",
            "data":None
        }
    except Exception as e:
        print(f"发送验证码出现异常：{e}")
        return {
            "code": 500,
            "msg":"发送验证码出现异常",
            "data":None
        }

def login(email, captcha):
    captcha = str(captcha)
    key = f"login:{email}"
    client = LoadRedis().redis_conn()
    code = client.get(key)
    if code is None:
        return {
            "code": 500,
            "msg":"验证码已过期",
            "data":None
        }
    try:
        if code != captcha:
            LoadRedis().redis_close(client)
            return {
                "code": 500,
                "msg":"验证码错误",
                "data":None
            }
        result = UsersDao.query_usersinfo_by_email(email)
        user = result[0]
        return {
            "code": 200,
            "msg":"登录成功",
            "data":{
                "user_id": user['users_id'],
                "nickname":user['nickname'],
                "email":user['email'],
                "email_password": user['email_password'],
                "roles_id": user['roles_id'],
            }
        }
    except Exception as e:
        print(f"登录出现异常：{e}")
        return {
            "code": 500,
            "msg":"登录异常",
            "data":None
        }

def register(RegisterEntity):
    em = UsersDao.query_usersinfo_by_email(RegisterEntity.email)
    if em:
        return {
            "code": 500,
            "msg":"邮箱已注册",
            "data":None
        }
    else:
        RegisterEntity.password = crypt_context.hash(RegisterEntity.password)
        rs = UsersDao.save_usersinfo_by_email(RegisterEntity)
        print("rs =", repr(rs), "type =", type(rs))
        if rs > 0:
            return {
                "code": 200,
                "msg":"注册成功",
                "data": rs
            }
        else:
            return {
                "code": 500,
                "msg": "注册失败",
                "data": None
            }

def password_login(email, password):
    user_info = UsersDao.query_usersinfo_by_email(email)
    if user_info:
        users_password = user_info[0]['password']
        user = user_info[0]
        if crypt_context.verify(password, users_password):
            return {
                "code": 200,
                "msg": "登录成功",
                "data": {
                    "user_id": user['users_id'],
                    "nickname": user['nickname'],
                    "email": user['email'],
                    "email_password": user['email_password'],
                    "roles_id": user['roles_id'],
                }
            }
        else:
            return {
                "code": 500,
                "msg":"登录异常",
                "data":None
            }
    else:
        return {
            "code": 500,
            "msg": "用户名不存在",
            "data": None
        }

if __name__ == '__main__':
    rs = password_login("3335281906@qq.com")
    print(rs)