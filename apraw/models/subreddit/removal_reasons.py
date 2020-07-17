from typing import TYPE_CHECKING, Dict

from ..helpers.apraw_base import aPRAWBase
from ...const import API_PATH

if TYPE_CHECKING:
    from .subreddit import Subreddit
    from ...reddit import Reddit


class SubredditRemovalReason(aPRAWBase):

    def __init__(self, reddit: 'Reddit', data: Dict):
        super().__init__(reddit, data)


class SubredditRemovalReasons:

    def __init__(self, subreddit: 'Subreddit'):
        self._subreddit = subreddit
        self._removal_reasons = list()

    async def _fetch(self):
        res = await self._subreddit._reddit.get_request(
            API_PATH["subreddit_removal_reasons"].format(sub=self._subreddit.display_name))

        for reason_id in res["order"]:
            self._removal_reasons.append(SubredditRemovalReason(self._subreddit._reddit, res["data"][reason_id]))

    async def get(self, item: str):
        if not self._removal_reasons:
            await self._fetch()

        next(reason for reason in self._removal_reasons if reason.id == item)

    async def __aiter__(self):
        if not self._removal_reasons:
            await self._fetch()

        return next(self._removal_reasons)
