from datetime import datetime

from pydantic import BaseModel, Field


class UserDataRespModel(BaseModel):
    id: str = Field(title="用户id")
    username: str = Field(title="用户名")
    realname: str = Field(title="昵称")
    enable: int = Field(title="用户状态")
    create_at: datetime = Field(title="添加时间")
    update_at: datetime = Field(title="修改时间")
    dept_name: str = Field(title="部门名称")
