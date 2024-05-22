from typing import TypeVar, Union, Generic, List

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

from pub.dto import PageModel

T = TypeVar('T', bound=Union[BaseModel])


class BaseTableRespModel(GenericModel, Generic[T], PageModel):
    """
    公共表格列表查询响应模型类
    """
    code: int = Field(default=0, title="响应码")
    msg: str = Field(title="响应信息")
    count: int = Field(default=0, title="总记录数")
    total_page: int = Field(default=0, title="总页数")
    data: List[T] = Field(title="响应数据")
