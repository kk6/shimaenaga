import math
from dataclasses import dataclass
from typing import Sequence, Optional, Iterator

from .contents import Content


def chunks(lst: Sequence, n: int) -> Iterator[Sequence]:
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


@dataclass
class Page:
    contents: Sequence[Content]
    prev_page: Optional[int]
    next_page: Optional[int]
    current_page: int


@dataclass
class Paginator:
    contents: Sequence[Content]
    per_page: int

    @property
    def num_of_pages(self) -> int:
        return math.ceil(len(self.contents) / self.per_page)

    def paginate(self) -> Iterator[Page]:
        for current_page, contents in enumerate(chunks(self.contents, self.per_page), start=1):
            if current_page == 1:
                prev_page = None
            else:
                prev_page = current_page - 1
            if current_page == self.num_of_pages:
                next_page = None
            else:
                next_page = current_page + 1
            yield Page(contents, prev_page, next_page, current_page)
