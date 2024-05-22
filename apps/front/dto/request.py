from typing import Optional

from pydantic import Field

from pub.dto import PageModel


class BookQueryModel(PageModel):
    """
    小说搜索查询dto
    """
    update_period: Optional[int] = Field(title="更新时间", alias='updatePeriod')
    work_direction: Optional[int] = Field(title="作品频道/创作方向", alias='workDirection')
    cat_id: Optional[int] = Field(title="分类id", alias='catId', gt=0)
    is_vip: Optional[int] = Field(title="是否收费", alias='isVip')
    book_status: Optional[int] = Field(title="是否完结", alias='bookStatus')
    word_count_min: Optional[int] = Field(title="字数大于等于", alias='wordCountMin', ge=0)
    word_count_max: Optional[int] = Field(title="字数小于等于", alias='wordCountMax', gt=0)
    keyword: Optional[str] = Field(default='', title="搜索关键词（作者名、小说名）")
    sort: Optional[str] = Field(default='update_time', title="排序方式")
    author_id: Optional[int] = Field(title="作者id", alias='authorId', gt=0)
