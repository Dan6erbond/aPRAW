from ..endpoints import API_PATH
from ..utils import snake_case_keys
from .apraw_base import aPRAWBase


class Comment(aPRAWBase):

    def __init__(self, reddit, data, submission=None,
                 author=None, subreddit=None):
        super().__init__(reddit, data)

        self._submission = submission
        self._author = author
        self._subreddit = subreddit

        self.subreddit_name = data["subreddit"]
        self.url = "https://www.reddit.com" + data["permalink"]

    async def author(self):
        if self._author is None:
            self._author = await self.reddit.redditor(self.data["author"])
        return self._author

    async def submission(self):
        if self._submission is None:
            link = await self.reddit.get_request(API_PATH["info"], id=self.data["link_id"])
            from .submission import Submission
            self._submission = Submission(
                self.reddit, link["data"]["children"][0]["data"])
        return self._submission

    async def subreddit(self):
        if self._subreddit is None:
            self._subreddit = await self.reddit.subreddit(self.subreddit_name)
        return self._subreddit
