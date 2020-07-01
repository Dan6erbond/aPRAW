import asyncio
from typing import TYPE_CHECKING, AsyncIterator, List

from .apraw_base import aPRAWBase
from .generator import ListingGenerator
from ..subreddit import Subreddit

if TYPE_CHECKING:
    from ...reddit import Reddit


class ListingStream:
    """
    The model to request and poll listings from Reddit.

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
                 max_wait: int = 16, kind_filter: List[str] = None,
                 subreddit: Subreddit = None):
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

    def get(self, limit: int = 25, **kwargs) -> AsyncIterator[aPRAWBase]:
        r"""
        Returns a :class:`~apraw.models.ListingGenerator` mapped to the given endpoints and other arguments.

        Parameters
        ----------
        limit: int
            The maximum amount of items to search. If ``None``, all are returned.
        kwargs: \*\*Dict
            Query parameters to append to the request URL.

        Returns
        -------
        generator: ListingGenerator
            A :class:`~apraw.models.ListingGenerator` instance with which items can be retrieved.
        """
        return ListingGenerator(self.reddit, self.endpoint, limit, self.subreddit, self.kind_filter, **kwargs)

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
        fullnames = list()

        if skip_existing:
            async for s in self.get(1, **kwargs):
                fullnames.append(s.fullname)
                break

        while True:
            found = False
            items = [i async for i in self.get(100, **kwargs)]
            for s in reversed(items):
                if s.fullname in fullnames:
                    break
                if len(fullnames) >= 301:
                    fullnames = fullnames[1:]
                fullnames.append(s.fullname)
                found = True
                yield s

            if found:
                wait = 1
            else:
                wait *= 2
                if wait > self.max_wait:
                    wait = 1

            await asyncio.sleep(wait)
