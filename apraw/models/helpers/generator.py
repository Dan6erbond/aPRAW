from typing import TYPE_CHECKING, AsyncIterator, Awaitable

from .apraw_base import aPRAWBase
from ..comment import Comment
from ..submission import Submission
from ..subreddit import ModAction, Subreddit
from ..subreddit_wiki import WikipageRevision

if TYPE_CHECKING:
    from ...reddit import Reddit


class ListingGenerator(AsyncIterator):
    """
    The model to request listings from Reddit.

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

    def __init__(self, reddit: 'Reddit', endpoint: str, limit: int = 100, subreddit: Subreddit = None, kind_filter=None,
                 **kwargs):
        r"""
        Create a ``ListingGenerator`` instance.

        Parameters
        ----------
        reddit: Reddit
            The :class:`~apraw.Reddit` instance with which requests are made.
        endpoint: str
            The endpoint to make requests on.
        limit: int
            The maximum number of items to fetch.
        max_wait: int
            The maximum amount of seconds to wait before re-requesting in streams.
        subreddit: Subreddit
            The subreddit to inject as a dependency into items if given.
        kwargs: \*\*Dict
            Query parameters to append to the request URL.
        """
        self.reddit = reddit
        self.endpoint = endpoint
        self.limit = limit if limit else 1024
        self.subreddit = subreddit
        self.params = kwargs
        self.listing = None
        self.kind_filter = kind_filter
        self._index = 0
        self._yielded = 0

    def __aiter__(self) -> AsyncIterator[aPRAWBase]:
        """
        Permit ListingGenerator to operate as an iterator.

        Returns
        -------
        self: ListingGenerator
            The iterator.
        """
        return self

    async def __anext__(self) -> Awaitable[aPRAWBase]:
        """
        Permit ListingGenerator to operate as a generator.

        Returns the next item in the listing.

        Returns
        -------
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
        if self.listing is not None and len(self.listing) == 0 or self._yielded >= self.limit:
            raise StopAsyncIteration()

        if self.listing is None or self._index >= len(self.listing):
            await self._next_batch()

        self._index += 1
        self._yielded += 1
        return self.listing[self._index - 1]

    async def _next_batch(self):
        """
        Retrieve the next batch of items and store them in a :class:`~apraw.models.Listing`.
        """
        if self.limit < 1:
            raise StopAsyncIteration()

        kwargs = {**self.params, "limit": self.limit}

        if self.listing:
            kwargs["after"] = self.listing.last.fullname

        self.listing = await self.reddit.get_listing(self.endpoint, self.subreddit, self.kind_filter, **kwargs)
        self.limit -= len(self.listing)

        if len(self.listing) <= 0:
            raise StopAsyncIteration()

        self._index = 0
