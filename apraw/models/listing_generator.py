import asyncio
from typing import TYPE_CHECKING, Any, AsyncIterator, Callable, List, Union

from ..utils import prepend_kind
from .apraw_base import aPRAWBase
from .comment import Comment
from .submission import Submission
from .subreddit import ModAction, Subreddit
from .subreddit_wiki import WikipageRevision

if TYPE_CHECKING:
    from ..reddit import Reddit


class ListingGenerator:

    def __init__(self, reddit: 'Reddit', endpoint: str,
                 max_wait: int = 16, kind_filter: List[str] = [],
                 subreddit=None):
        self.reddit = reddit
        self.endpoint = endpoint
        self.max_wait = max_wait
        self.kind_filter = kind_filter
        self.subreddit = subreddit

    @classmethod
    def get_listing_generator(cls, reddit: 'Reddit', endpoint: str,
                              max_wait: int = 16, kind_filter: List[str] = [],
                              subreddit=None) -> Callable[[Any], AsyncIterator[aPRAWBase]]:
        async def get_listing(limit: int = 25, **kwargs) -> AsyncIterator[aPRAWBase]:
            last = None
            while True:
                kwargs["limit"] = limit if limit is not None else 100
                if last is not None:
                    kwargs["after"] = last
                req = await reddit.get_request(endpoint, **kwargs)
                if len(req["data"]["children"]) <= 0:
                    break
                for i in req["data"]["children"]:
                    wiki_page = "page" in i

                    if wiki_page and kind_filter and reddit.wiki_revision_kind not in kind_filter:
                        continue
                    elif not wiki_page and kind_filter and i["kind"] in kind_filter:
                        continue

                    if wiki_page:
                        last = prepend_kind(i["id"], reddit.wiki_revision_kind)
                    elif i["kind"] in [reddit.link_kind,
                                       reddit.subreddit_kind, reddit.comment_kind]:
                        last = i["data"]["name"]
                    elif i["kind"] == reddit.modaction_kind:
                        last = i["data"]["id"]

                    if limit is not None:
                        limit -= 1

                    if wiki_page:
                        yield WikipageRevision(reddit, i)
                    elif i["kind"] == reddit.link_kind:
                        yield Submission(reddit, i["data"], subreddit=subreddit)
                    elif i["kind"] == reddit.subreddit_kind:
                        yield Subreddit(reddit, i["data"])
                    elif i["kind"] == reddit.comment_kind:
                        yield Comment(reddit, i["data"], subreddit=subreddit)
                    elif i["kind"] == reddit.modaction_kind:
                        yield ModAction(i["data"], subreddit)
                    else:
                        yield aPRAWBase(i["data"] if "data" in i else i)
                if limit is not None and limit < 1:
                    break

        return get_listing

    async def get(self, *args, **kwargs) -> AsyncIterator[aPRAWBase]:
        async for i in ListingGenerator.get_listing_generator(**vars(self))(*args, **kwargs):
            yield i

    __call__ = get

    async def stream(self, **kwargs) -> AsyncIterator[aPRAWBase]:
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
