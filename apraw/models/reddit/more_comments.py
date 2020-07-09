from typing import TYPE_CHECKING, Dict, Any, List, Union

from .comment import Comment
from .submission import Submission
from ..helpers.apraw_base import aPRAWBase
from ...const import API_PATH

if TYPE_CHECKING:
    from ...reddit import Reddit


class MoreComments(aPRAWBase):

    def __init__(self, reddit: 'Reddit', data: Dict[str, Any], link_id: str):
        data.update(link_id=link_id)
        super().__init__(reddit, data)

        self._comments = []
        self._ids = list(self.children)
        self._index = 0

    async def _next_batch(self):
        if not self._ids:
            return

        ids = self._ids[:100]
        self._ids = self._ids[100:]
        resp = await self._reddit.get_request(API_PATH["morechildren"], **{
            "children": ",".join(ids),
            "link_id": self.link_id,
            "id": self.id,
            "depth": self.depth
        })

        from .listing import MoreChildren
        children = MoreChildren(self._reddit, resp["json"]["data"], [self._reddit.comment_kind, self._reddit.more_kind],
                                self.link_id)
        self._comments.extend(comment for comment in children)

    async def parent(self) -> Union[Submission, Comment]:
        return await self._reddit.info(self.parent_id)

    async def fetch(self):
        while self._ids:
            await self._next_batch()

    async def __anext__(self) -> Comment:
        if self._index >= len(self._comments) and not self._ids:
            raise StopAsyncIteration

        if not self._comments or self._ids:
            await self._next_batch()

        self._index += 1
        return self._comments[self._index + 1]

    async def comments(self) -> List[Comment]:
        if not self._comments:
            await self.fetch()

        return self._comments
