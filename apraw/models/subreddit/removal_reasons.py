from typing import TYPE_CHECKING, Dict, Optional

from ..helpers.apraw_base import aPRAWBase
from ...const import API_PATH

if TYPE_CHECKING:
    from .subreddit import Subreddit
    from ...reddit import Reddit


class SubredditRemovalReason(aPRAWBase):

    def __init__(self, reddit: 'Reddit', subreddit: 'Subreddit', data: Dict):
        self._subreddit = subreddit
        super().__init__(reddit, data)
        self.url = API_PATH["subreddit_removal_reason"].format(sub=self._subreddit.display_name, id=self.id)

    async def fetch(self):
        url = API_PATH["subreddit_removal_reasons"].format(sub=self._subreddit.display_name)
        res = await self._reddit.get(url)
        super()._update(res["data"][self.id])

    async def delete(self):
        res = await self._reddit.delete(self.url)
        return res

    async def update(self, title: Optional[str] = None, message: Optional[str] = None):
        data = {
            k: v if v else getattr(self, k)
            for k, v in {"message": message, "title": title}.items()
        }
        await self._reddit.put(self.url, data=data)


class SubredditRemovalReasons:

    def __init__(self, reddit: 'Reddit', subreddit: 'Subreddit'):
        self._reddit = reddit
        self._subreddit = subreddit
        self._removal_reasons = list()
        self._index = 0

    async def _fetch(self):
        url = API_PATH["subreddit_removal_reasons"].format(sub=self._subreddit.display_name)
        res = await self._reddit.get(url)

        for reason_id in res["order"]:
            reason = SubredditRemovalReason(self._reddit, self._subreddit, res["data"][reason_id])
            self._removal_reasons.append(reason)

    async def get(self, item: str):
        if not self._removal_reasons:
            await self._fetch()

        next(reason for reason in self._removal_reasons if reason.id == item)

    def __aiter__(self):
        return self

    async def __anext__(self):
        if not self._removal_reasons:
            await self._fetch()

        if self._index >= len(self._removal_reasons):
            raise StopAsyncIteration

        self._index += 1
        return self._removal_reasons[self._index - 1]

    async def add(self, title: str, message: str) -> SubredditRemovalReason:
        data = {"message": message, "title": title}
        url = API_PATH["subreddit_removal_reasons"].format(sub=self._subreddit.display_name)

        data = await self._reddit.post(url, data=data)

        reason = SubredditRemovalReason(self._reddit, self._subreddit, data)
        await reason.fetch()
        return reason
