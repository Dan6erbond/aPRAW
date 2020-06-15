from datetime import datetime

from ..endpoints import API_PATH
from ..utils import snake_case_keys
from .comment import Comment
from .submission import Submission
from .subreddit import Subreddit


class Redditor:
    def __init__(self, reddit, data):
        self.reddit = reddit
        self.data = data

        if "is_suspended" not in data or not data["is_suspended"]:
            self.is_suspended = False
            self.created_utc = datetime.utcfromtimestamp(data["created_utc"])
        else:
            self.is_suspended = True

        d = snake_case_keys(data)
        for key in d:
            if not hasattr(self, key):
                setattr(self, key, d[key])

        if "subreddit" in data and data["subreddit"]:
            sub = data["subreddit"]
            sub["id"] = sub["name"].replace("t5_", "")
            if "created_utc" not in sub:
                sub["created_utc"] = data["created_utc"]
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

    async def moderated_subreddits(self, **kwargs):
        req = await self.reddit.get_request(API_PATH["moderated"].format(user=self), **kwargs)
        for s in req["data"]:
            yield await self.reddit.subreddit(s["sr"])

    async def message(self, subject, text, from_sr=""):
        return await self.reddit.message(self.name, subject, text, from_sr)
