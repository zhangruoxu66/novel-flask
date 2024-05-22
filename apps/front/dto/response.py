from datetime import datetime
from typing import List

from pydantic import BaseModel


class BookQueryResp(BaseModel):
    id: str
    cat_id: int
    cat_name: str
    book_name: str
    author_id: int
    author_name: str
    word_count: int
    last_index_id: str
    last_index_name: str
    score: float
    pic_url: str
    book_status: int
    last_index_update_time: datetime
    book_desc: str


class BookQueryRespModel(BaseModel):
    """
    小说搜索查询响应dto
    """
    data: List[BookQueryResp]
    count: int
    page: int
    limit: int
