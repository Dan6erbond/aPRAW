import asyncio
from typing import TYPE_CHECKING, Any, AsyncIterator, Callable, List

from ...utils import prepend_kind
from ..comment import Comment
from ..submission import Submission
from ..subreddit import ModAction, Subreddit
from ..subreddit_wiki import WikipageRevision
from .apraw_base import aPRAWBase
from .listing import Listing

if TYPE_CHECKING:
    from ...reddit import Reddit


class ListingGenerator:
    """
    The model to request, parse and poll listings from Reddit.

    Members
    -------
    reddit: Reddit
        The :class:`~apraw.Reddit` instance with which requests are made.
    endpoint: str
        The endpoint to make requests on.
    max_wait: int
        The maximum amount of seconds to wait before re-requesting in streams.
    kind_filter:
        Kinds to return if given, otherwise all are returned.
    subreddit: Subreddit
        The subreddit to inject as a dependency into items if given.

    .. note::
        ListingGenerator will automatically make requests until none more are found or the limit has been reached.
    """

    def __init__(self, reddit: 'Reddit', endpoint: str,
                 max_wait: int = 16, kind_filter: List[str] = [],
                 subreddit=None):
        """
        Create a ListingGenerator instance.

        Parameters
        ----------
        reddit: Reddit
            The :class:`~apraw.Reddit` instance with which requests are made.
        endpoint: str
            The endpoint to make requests on.
        max_wait: int
            The maximum amount of seconds to wait before re-requesting in streams.
        kind_filter:
            Kinds to return if given, otherwise all are returned.
        subreddit: Subreddit
            The subreddit to inject as a dependency into items if given.
        """
        self.reddit = reddit
        self.endpoint = endpoint
        self.max_wait = max_wait
        self.kind_filter = kind_filter
        self.subreddit = subreddit

    async def get(self, limit: int = 25, **kwargs) -> AsyncIterator[aPRAWBase]:
        r"""
        Yields items found in the listing.

        Parameters
        ----------
        limit: int
            The maximum amount of items to search. If ``None``, all are returned.
        kwargs: \*\*Dict
            Query parameters to append to the request URL.

        Yields
        ------
        subreddit: Subreddit
            The subreddit found in the listing.
        comment: Comment
            The comment found in the listing.
        submission: Submission
            The submission found in the listing.
        mod_action: ModAction
            The mod action found in the listing.
        wikipage_revision: WikipageRevision
            The wikipage revision found in the listing.
        item: aPRAWBase
            A model of the item's data if kind couldn't be identified.
        """
        last = None

        while True:
            kwargs["limit"] = limit if limit is not None else 100

            if last:
                kwargs["after"] = last

            listing = await self.reddit.get_listing(self.endpoint, self.subreddit, **kwargs)

            if len(listing) <= 0:
                break

            last = listing.last.fullname

            for item in listing:
                if self.kind_filter and item.kind not in self.kind_filter:
                    continue

                if limit is not None:
                    limit -= 1

                yield item

            if limit is not None and limit < 1:
                break

    __call__ = get

    async def stream(self, skip_existing: bool = False, **kwargs) -> AsyncIterator[aPRAWBase]:
        r"""
        Stream items from an endpoint.

        Streams use the ``asyncio.sleep()`` call to wait in between requests.
        If no items are found, the wait time is double until ``max_wait`` has been reached, at which point it's reset to 1.

        Parameters
        ----------
        skip_existing: bool
            Whether to skip items made before the call.
        kwargs: \*\*Dict
            Query parameters to append to the request URL.

        Yields
        ------
        subreddit: Subreddit
            The subreddit found in the listing.
        comment: Comment
            The comment found in the listing.
        submission: Submission
            The submission found in the listing.
        mod_action: ModAction
            The mod action found in the listing.
        wikipage_revision: WikipageRevision
            The wikipage revision found in the listing.
        item: aPRAWBase
            A model of the item's data if kind couldn't be identified.
        """
        wait = 0
        ids = list()

        if skip_existing:
            async for s in self.get(1, **kwargs):
                ids.append(s.id)
                break

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
