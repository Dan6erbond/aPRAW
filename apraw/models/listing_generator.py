import asyncio
from typing import *

import apraw

from .comment import Comment
from .submission import Submission
from .subreddit import ModAction, Subreddit


class ListingGenerator:

    def __init__(self, reddit: apraw.Reddit, endpoint: str,
                 max_wait: int = 16, kind_filter: List[str] = []):
        self.reddit = reddit
        self.endpoint = endpoint
        self.max_wait = max_wait
        self.kind_filter = kind_filter

    async def get(self, limit=25, **kwargs):
        reddit = self.reddit
        last = None

        while True:
            kwargs["limit"] = limit if limit is not None else 100
            if last is not None:
                kwargs["after"] = last
            req = await reddit.get_request(self.endpoint, **kwargs)
            if len(req["data"]["children"]) <= 0:
                break
            for i in req["data"]["children"]:
                if i["kind"] in [reddit.link_kind,
                                 reddit.subreddit_kind, reddit.comment_kind]:
                    last = i["data"]["name"]
                elif i["kind"] == reddit.modaction_kind:
                    last = i["data"]["id"]

                if limit is not None:
                    limit -= 1

                if len(
                        self.kind_filter) > 0 and i["kind"] not in self.kind_filter:
                    continue

                if i["kind"] == reddit.link_kind:
                    yield Submission(reddit, i["data"])
                elif i["kind"] == reddit.subreddit_kind:
                    yield Subreddit(self.reddit, i["data"])
                elif i["kind"] == reddit.comment_kind:
                    yield Comment(self.reddit, i["data"])
                elif i["kind"] == reddit.modaction_kind:
                    yield ModAction(self.reddit, i["data"])
            if limit is not None and limit < 1:
                break

    __call__ = get

    async def stream(self, **kwargs):
        wait = 0
        ids = list()

        while True:
            found = False
            async for s in self.get(100, **kwargs):
                if s.id in ids:
                    break
                if len(ids) >= 301:
                    ids = ids[1:]
                ids.append(s.id)
                found = True
                yield s

            if found:
                wait = 1
            else:
                wait *= 2
                if wait > self.max_wait:
                    wait = 1

            await asyncio.sleep(wait)