from typing import Optional

from pydantic import BaseModel, Field


class PageModel(BaseModel):
    page: Optional[int] = Field(default=1, title="页码")
    limit: Optional[int] = Field(default=10, title="每页条数")
