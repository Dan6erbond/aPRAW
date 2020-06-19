from typing import TYPE_CHECKING, AsyncIterator, Dict, List

from ..endpoints import API_PATH
from ..utils import snake_case_keys
from .apraw_base import aPRAWBase
from .comment import Comment
from .redditor import Redditor
from .subreddit import Subreddit

if TYPE_CHECKING:
    from ..reddit import Reddit


class Submission(aPRAWBase):
    def __init__(self, reddit: 'Reddit', data: Dict, full_data: Dict = None,
                 subreddit: Subreddit = None, author: Redditor = None):
        super().__init__(reddit, data)

        self._full_data = full_data
        self._comments = list()
        self._subreddit = subreddit
        self._author = author

        self.original_content = data["is_original_content"]

    async def full_data(self) -> Dict:
        if self._full_data is None:
            sub = await self.subreddit()
            self._full_data = await self.reddit.get_request(API_PATH["submission"].format(sub=sub.display_name, id=self.id))
        return self._full_data

    async def comments(self, reload=False, **kwargs) -> AsyncIterator[Comment]:
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

    async def morechildren(self, children) -> List[Comment]:
        comments = list()

        while len(children) > 0:
            cs = children[:100]
            children = children[100:]

            def get_comments(comment_list, comments):
                for i in comment_list:
                    if isinstance(i, list):
                        comments = get_comments(i, comments)
                    elif isinstance(i, dict) and "kind" in i and i["kind"] == self.reddit.comment_kind:
                        comments.append(
                            Comment(self.reddit, i["data"], submission=self))
                return comments

            data = await self.reddit.get_request(API_PATH["morechildren"], children=",".join(cs), link_id=self.name)
            comments = get_comments(data["jquery"], comments)

        return comments

    async def subreddit(self) -> Subreddit:
        if self._subreddit is None:
            self._subreddit = await self.reddit.subreddit(self.data["subreddit"])
        return self._subreddit

    async def author(self) -> Subreddit:
        if self._author is None:
            self._author = await self.reddit.redditor(self.data["author"])
        return self._author
