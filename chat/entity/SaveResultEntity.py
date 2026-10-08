from pydantic import BaseModel,Field

class SaveResultEntity(BaseModel):
    usersId:int = Field(...,description="用户id")
    question:str = Field(...,description="用户问题")
    answer:str = Field(...,description="系统回答")
    parentId:int = Field(...,description="父子id")