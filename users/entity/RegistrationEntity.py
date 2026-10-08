from pydantic import BaseModel,Field

class RegisterEntity(BaseModel):
    email: str = Field(...,description="用户邮箱")
    nickname: str = Field(...,description="用户昵称")
    password: str = Field(...,description="用户密码")
    email_password: str = Field(default="",description="邮箱授权码")
    roles_id: int = Field(default=int(0),description="角色id")
