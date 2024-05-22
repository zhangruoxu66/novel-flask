from typing import Optional

from pydantic import BaseModel, Field

from pub.dto import PageModel


class AdminUserQueryModel(PageModel):
    """
    管理员列表查询dto
    """
    real_name: Optional[str] = Field(title="昵称", alias='realName')
    username: Optional[str] = Field(title="用户名")
    dept_id: Optional[int] = Field(title="部门id", gt=0, alias='deptId')


class AdminUserAddModel(BaseModel):
    """
    添加管理员dto
    """
    role_ids: str = Field(default='', title="角色id列表", alias='roleIds')
    username: str = Field(title="用户名")
    real_name: str = Field(title="昵称", alias='realName')
    password: str = Field(title="密码")


class AdminUserUpdateModel(BaseModel):
    """
    修改管理员dto
    """
    role_ids: str = Field(default='', title="角色id列表", alias='roleIds')
    user_id: int = Field(title="管理员id", gt=0, alias='userId')
    username: str = Field(title="用户名")
    real_name: str = Field(title="昵称", alias='realName')
    dept_id: Optional[int] = Field(title="部门id", gt=0, alias='deptId')
