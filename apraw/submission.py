from datetime import datetime

from .comment import Comment


class Submission:

    def __init__(self, reddit, data, full_data=None, subreddit=None, author=None):
        self.reddit = reddit
        self.data = data

        self._full_data = full_data
        self._comments = list()
        self._subreddit = subreddit
        self._author = author

        self.id = data["id"]
        self.created_utc = datetime.utcfromtimestamp(data["created_utc"])

        self.name = data["name"]
        self.title = data["title"]
        self.selftext = data["selftext"]
        self.media = data["media"]
        self.over18 = data["over_18"]
        self.is_video = data["is_video"]
        self.original_content = data["is_original_content"]
        self.score = data["score"]
        self.stickied = data["stickied"]
        self.archived = data["archived"]
        self.locked = data["locked"]
        self.permalink = data["permalink"]
        self.url = data["url"]

        self.pinned = data["pinned"] # indicates if the post is pinned on the user's profile

        self.user_reports = data["user_reports"]
        self.mod_reports = data["mod_reports"]

    async def full_data(self):
        if self._full_data is None:
            sub = await self.subreddit()
            self._full_data = await self.reddit.get_request("/r/{}/comments/{}".format(sub.display_name, self.id))

        return self._full_data

    async def comments(self, **kwargs):
        if len(self._comments) <= 0:
            fd = await self.full_data()
            for c in fd[1]["data"]["children"]:
                if c["kind"] == self.reddit.comment_kind: self._comments.append(Comment(self.reddit, c["data"], submission=self))
        for c in self._comments:
            yield c

    async def subreddit(self):
        if self._subreddit is None:
            self._subreddit = await self.reddit.subreddit(self.data["subreddit"])
        return self._subreddit

    async def author(self):
        if self._author is None:
            self._author = await self.reddit.redditor(self.data["author"])
        return self._author