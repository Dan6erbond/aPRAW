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

    async def delete(self):
        url = API_PATH["subreddit_removal_reason"].format(sub=self._subreddit.display_name, id=self.id)
        res = await self._reddit.delete(url)
        return res

    async def update(self, message: Optional[str] = None, title: Optional[str] = None):
        url = API_PATH["subreddit_removal_reason"].format(sub=self._subreddit.display_name, id=self.id)
        data = {
            k: v if v else getattr(self, k)
            for k, v in {"message": message, "title": title}.items()
        }
        await self._reddit.put(url, data=data)


class SubredditRemovalReasons:

    def __init__(self, reddit: 'Reddit', subreddit: 'Subreddit'):
        self._reddit = reddit
        self._subreddit = subreddit
        self._removal_reasons = list()

    async def _fetch(self):
        url = API_PATH["subreddit_removal_reasons"].format(sub=self._subreddit.display_name)
        res = await self._reddit.get(url)

        for reason_id in res["order"]:
            self._removal_reasons.append(SubredditRemovalReason(self._reddit, res["data"][reason_id]))

    async def get(self, item: str):
        if not self._removal_reasons:
            await self._fetch()

        next(reason for reason in self._removal_reasons if reason.id == item)

    async def __aiter__(self):
        if not self._removal_reasons:
            await self._fetch()

        return next(self._removal_reasons)
