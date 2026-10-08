from email.mime.text import MIMEText
import smtplib
from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_headers
from common import Jwtutils
from users.dao import UsersDao

mcp = FastMCP("email-server")

@mcp.tool(name="send_email_tool")
def send_email_tool(to:str,subject:str,content:str, user_token: str = "")->str:
    """
    功能描述：发送邮件，发送信息，发送通知
    """
    try:
        if not user_token:
            return "缺少用户身份凭证，无法发送邮件"
        try:
            payload = Jwtutils.verify_token(user_token)
        except Exception:
            return "用户身份已失效，请重新登录"
        users_id = payload.get("usersId")
        user_infomation = UsersDao.query_usersinfo_by_usersId(users_id)
        email_user = user_infomation[0]["email"]
        email_password = user_infomation[0]["email_password"]
        host = "smtp.qq.com"
        user =  email_user
        password = email_password
        port = 465
        if not host or not user or not password or not port:
            return "请检查邮件配置"
        msg = MIMEText(content)
        msg["To"] = to
        msg["Subject"] = subject
        msg["From"] = user
        with smtplib.SMTP_SSL(host,int(port)) as smtp:
            smtp.login(user,password)
            smtp.sendmail(msg["From"],msg["To"],msg.as_string())
        return "邮件发送成功"
    except Exception as e:
        print(f"出现异常{e}")
        return "发送邮件异常"

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="localhost", port=9000)