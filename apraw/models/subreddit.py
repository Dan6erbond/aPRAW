import asyncio
from datetime import datetime
from typing import TYPE_CHECKING, AsyncIterator, Dict, List

from ..endpoints import API_PATH
from ..utils import snake_case_keys
from .apraw_base import aPRAWBase
from .modmail import SubredditModmail
from .redditor import Redditor
from .subreddit_wiki import SubredditWiki

if TYPE_CHECKING:
    from ..reddit import Reddit


class Subreddit(aPRAWBase):

    def __init__(self, reddit: 'Reddit', data: Dict):
        super().__init__(reddit, data)

        self.quarantine = data["quarantine"] if "quarantine" in data else False

        self.mod = SubredditModeration(self)
        self.modmail = SubredditModmail(self)
        self.wiki = SubredditWiki(self)

        from .listing_generator import ListingGenerator
        self.comments = ListingGenerator(
            self.reddit, API_PATH["subreddit_comments"].format(
                sub=self.display_name), subreddit=self)
        self.new = ListingGenerator(self.reddit,
                                    API_PATH["subreddit_new"].format(sub=self.display_name), subreddit=self)
        self.hot = ListingGenerator(self.reddit,
                                    API_PATH["subreddit_hot"].format(sub=self.display_name), subreddit=self)
        self.rising = ListingGenerator(
            self.reddit, API_PATH["subreddit_rising"].format(sub=self.display_name))
        self.top = ListingGenerator(self.reddit,
                                    API_PATH["subreddit_top"].format(sub=self.display_name), subreddit=self)

    def __str__(self):
        return self.display_name

    async def moderators(self, **kwargs) -> AsyncIterator['SubredditModerator']:
        req = await self.reddit.get_request(API_PATH["subreddit_moderators"].format(sub=self.display_name), **kwargs)
        for u in req["data"]["children"]:
            yield SubredditModerator(self.reddit, u)

    async def message(self, subject, text, from_sr="") -> Dict:
        return await self.reddit.message(API_PATH["subreddit"].format(sub=self.display_name), subject, text, from_sr)


class SubredditModerator(aPRAWBase):

    def __init__(self, reddit: 'Reddit', data: Dict):
        super().__init__(reddit, data)

        self.added = data["date"]

    def __str__(self):
        return self.name

    async def redditor(self) -> Redditor:
        return await self.reddit.redditor(self.name)


class SubredditModeration:

    def __init__(self, subreddit):
        self.subreddit = subreddit

        from .listing_generator import ListingGenerator
        self.reports = ListingGenerator(
            self.subreddit.reddit,
            API_PATH["subreddit_reports"].format(
                sub=self.subreddit.display_name), subreddit=self.subreddit)
        self.spam = ListingGenerator(
            self.subreddit.reddit,
            API_PATH["subreddit_spam"].format(
                sub=self.subreddit.display_name), subreddit=self.subreddit)
        self.modqueue = ListingGenerator(
            self.subreddit.reddit,
            API_PATH["subreddit_modqueue"].format(
                sub=self.subreddit.display_name), subreddit=self.subreddit)
        self.unmoderated = ListingGenerator(
            self.subreddit.reddit,
            API_PATH["subreddit_unmoderated"].format(
                sub=self.subreddit.display_name), subreddit=self.subreddit)
        self.edited = ListingGenerator(
            self.subreddit.reddit,
            API_PATH["subreddit_edited"].format(
                sub=self.subreddit.display_name), subreddit=self.subreddit)
        self.log = ListingGenerator(
            self.subreddit.reddit,
            API_PATH["subreddit_log"].format(
                sub=self.subreddit.display_name), subreddit=self.subreddit)


class ModAction:

    def __init__(self, data, subreddit=None):
        self.data = data
        self.subreddit = subreddit

        self.created_utc = datetime.utcfromtimestamp(data["created_utc"])

        d = snake_case_keys(data)
        for key in d:
            if not hasattr(self, key):
                setattr(self, key, d[key])

    async def mod(self) -> Redditor:
        return await self.subreddit.reddit.redditor(self.mod)
