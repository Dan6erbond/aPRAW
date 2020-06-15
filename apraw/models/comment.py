from datetime import datetime

from ..endpoints import API_PATH


class Comment:

    def __init__(self, reddit, data, submission=None, author=None, subreddit=None):
        self.reddit = reddit
        self.data = data

        self._submission = submission
        self._author = author
        self._subreddit = subreddit

        self.id = data["id"]
        self.created_utc = datetime.utcfromtimestamp(data["created_utc"])

        self.edited = data["edited"]
        self.archived = data["archived"]
        self.link_id = data["link_id"]
        self.parent_id = data["parent_id"]
        self.subreddit_name = data["subreddit"]
        self.subreddit_id = data["subreddit_id"]
        self.score = data["score"]
        self.body = data["body"]
        self.is_submitter = data["is_submitter"]
        self.url = "https://www.reddit.com" + data["permalink"]

        self.user_reports = data["user_reports"]
        self.mod_reports = data["mod_reports"]

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
