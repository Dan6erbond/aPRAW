from datetime import datetime

class Comment:

    def __init__(self, reddit, data, submission=None, author=None):
        self.reddit = reddit
        self.data = data

        self._submission = submission
        self._author = author

        self.id = data["id"]
        self.created_utc = datetime.utcfromtimestamp(data["created_utc"])

        self.edited = data["edited"]
        self.archived = data["archived"]
        self.parent_id = data["parent_id"]
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
            link = await self.reddit.get_request("/api/info", id=self.data["link_id"])
            from .submission import Submission
            self._submission = Submission(self.reddit, link["data"]["children"][0]["data"])
        return self._submission