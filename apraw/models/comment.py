from typing import TYPE_CHECKING, AsyncIterator, Dict, List

from ..endpoints import API_PATH
from ..utils import snake_case_keys
from .apraw_base import aPRAWBase
from .redditor import Redditor
from .subreddit import Subreddit

if TYPE_CHECKING:
    from ..reddit import Reddit
    from .submission import Submission


class Comment(aPRAWBase):

    def __init__(self, reddit: 'Reddit', data: Dict, submission: 'Submission' = None,
                 author: Redditor = None, subreddit: Subreddit = None, replies: List['Comment'] = None):
        super().__init__(reddit, data)

        self._submission = submission
        self._author = author
        self._subreddit = subreddit
        self._full_data = None
        self._replies = replies

        self.subreddit_name = data["subreddit"]
        self.url = "https://www.reddit.com" + data["permalink"]

    async def author(self) -> Redditor:
        if self._author is None:
            self._author = await self.reddit.redditor(self.data["author"])
        return self._author

    async def submission(self) -> 'Submission':
        if self._submission is None:
            link = await self.reddit.get_request(API_PATH["info"], id=self.data["link_id"])
            from .submission import Submission
            self._submission = Submission(
                self.reddit, link["data"]["children"][0]["data"])
        return self._submission

    async def subreddit(self) -> Subreddit:
        if self._subreddit is None:
            self._subreddit = await self.reddit.subreddit(self.subreddit_name)
        return self._subreddit

    async def full_data(self, refresh: bool = False) -> Dict:
        if self._full_data is None or refresh:
            self._full_data = await self.reddit.get_request(
                API_PATH["comment"].format(sub=self.data["subreddit"],
                                           submission=self.data["link_id"].replace(
                                               self.reddit.link_kind + "_", ""),
                                           id=self.data["id"]))
        return self._full_data

    async def refresh(self):
        await self.full_data(True)
        await self.replies(True)

    async def replies(self, refresh: bool = False) -> AsyncIterator['Comment']:
        if self._replies is None or refresh:
            fd = await self.full_data()

            def find(listing):
                data = listing["data"]

                for comment in data["children"]:
                    if comment["data"]["id"] == self.id:
                        return comment
                    else:
                        return find(comment["replies"])

            comment = find(fd[1])

            def get_replies(comment, replies=[]):
                if "kind" in comment["replies"] and comment["replies"]["kind"] == self.reddit.listing_kind:
                    for reply in comment["replies"]["data"]["children"]:
                        data = reply["data"]
                        replies.append(
                            Comment(self.reddit, data, replies=get_replies(data, [])))
                return replies

            self._replies = get_replies(comment["data"])

        for reply in self._replies:
            yield reply
