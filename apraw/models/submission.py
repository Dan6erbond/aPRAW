from datetime import datetime

from ..endpoints import API_PATH
from ..utils import snake_case_keys
from .comment import Comment


class Submission:

    def __init__(self, reddit, data, full_data=None,
                 subreddit=None, author=None):
        self.reddit = reddit
        self.data = data

        self._full_data = full_data
        self._comments = list()
        self._subreddit = subreddit
        self._author = author

        self.created_utc = datetime.utcfromtimestamp(data["created_utc"])
        self.original_content = data["is_original_content"]

        d = snake_case_keys(data)
        for key in d:
            if not hasattr(self, key):
                setattr(self, key, d[key])

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
                    self._comments.append(
                        Comment(
                            self.reddit,
                            c["data"],
                            submission=self))
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
                                    if isinstance(
                                            c, dict) and "kind" in c and c["kind"] == self.reddit.comment_kind:
                                        comments.append(
                                            Comment(
                                                self.reddit,
                                                c["data"],
                                                submission=self))

        return comments

    async def subreddit(self):
        if self._subreddit is None:
            self._subreddit = await self.reddit.subreddit(self.data["subreddit"])
        return self._subreddit

    async def author(self):
        if self._author is None:
            self._author = await self.reddit.redditor(self.data["author"])
        return self._author
