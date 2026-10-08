from pydantic import BaseModel,Field

class UpdateEntity(BaseModel):
    nickname: str = Field(...,description="用户昵称")
    password: str = Field(...,description="用户密码")
    roles_id: int = Field(default=int(0),description="角色id")
    email_password: str = Field(default="",description="邮箱授权码")
