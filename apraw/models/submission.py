from datetime import datetime

from ..endpoints import API_PATH
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
            self._full_data = await self.reddit.get_request(API_PATH["submission"].format(sub=sub.display_name, id=self.id))
        return self._full_data

    async def comments(self, reload=False, **kwargs):
        if len(self._comments) <= 0 or reload:
            fd = await self.full_data()
            self._comments = list()

            for c in fd[1]["data"]["children"]:
                if c["kind"] == self.reddit.comment_kind:
                    self._comments.append(Comment(self.reddit, c["data"], submission=self))
                if c["kind"] == "more":
                    self._comments.extend(await self.morechildren(c["data"]["children"]))
        for c in self._comments:
            yield c

    async def morechildren(self, children):
        comments = list()

        while len(children) > 0:
            cs = children[:100]
            children = children[100:]

            data = await self.reddit.get_request(API_PATH["morechildren"], children=",".join(cs), link_id=self.name)
            for l in data["jquery"]:
                for _l in l:
                    if isinstance(_l, list):
                        for cl in _l:
                            if isinstance(cl, list):
                                for c in cl:
                                    if isinstance(c, dict) and "kind" in c and c["kind"] == self.reddit.comment_kind:
                                        comments.append(Comment(self.reddit, c["data"], submission=self))

        return comments

    async def subreddit(self):
        if self._subreddit is None:
            self._subreddit = await self.reddit.subreddit(self.data["subreddit"])
        return self._subreddit

    async def author(self):
        if self._author is None:
            self._author = await self.reddit.redditor(self.data["author"])
        return self._author
