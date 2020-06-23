from typing import TYPE_CHECKING, Dict

from ..endpoints import API_PATH
from .apraw_base import aPRAWBase

if TYPE_CHECKING:
    from .subreddit import Subreddit
    from ..reddit import Reddit


class Redditor(aPRAWBase):
    def __init__(self, reddit: 'Reddit', data: Dict):
        super().__init__(reddit, data)

        self.reddit = reddit
        self.data = data

        self.is_suspended = "is_suspended" not in data or not data["is_suspended"]

        if "subreddit" in data and data["subreddit"]:
            sub = data["subreddit"]
            sub["id"] = sub["name"].replace("t5_", "")
            if "created_utc" not in sub:
                sub["created_utc"] = data["created_utc"]
            from .subreddit import Subreddit
            self.subreddit = Subreddit(self.reddit, sub)
        else:
            self.subreddit = None

        from .listing_generator import ListingGenerator
        self.comments = ListingGenerator(
            self.reddit,
            API_PATH["user_comments"].format(
                user=self))
        self.submissions = ListingGenerator(
            self.reddit,
            API_PATH["user_submissions"].format(
                user=self))

    def __str__(self):
        return self.name

    async def moderated_subreddits(self, **kwargs) -> 'Subreddit':
        req = await self.reddit.get_request(API_PATH["moderated"].format(user=self), **kwargs)
        for s in req["data"]:
            yield await self.reddit.subreddit(s["sr"])

    async def message(self, subject, text, from_sr="") -> Dict:
        return await self.reddit.message(self.name, subject, text, from_sr)
