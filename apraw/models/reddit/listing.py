from typing import TYPE_CHECKING, Dict, Iterator, List

from .comment import Comment
from .message import Message
from .more_comments import MoreComments
from .submission import Submission
from ..helpers.apraw_base import aPRAWBase
from ..subreddit.moderation import ModAction
from ..subreddit.subreddit import Subreddit
from ..subreddit.wiki import WikipageRevision

if TYPE_CHECKING:
    from ...reddit import Reddit


class Listing(aPRAWBase, Iterator):
    """
    A model representing Reddit listings.

    Members
    -------
    reddit: Reddit
        The :class:`~apraw.Reddit` instance with which requests are made.
    data: Dict
        The data retrieved from the endpoint.
    kind_filter:
        Kinds to return if given, otherwise all are returned.
    subreddit: Subreddit
        The subreddit to inject into items as their owner.
    CHILD_ATTRIBUTE: str
        The attribute in the data that contains the listing's items.
    """

    CHILD_ATTRIBUTE = "children"

    def __init__(self, reddit: 'Reddit', data: Dict, kind_filter: List[str] = None,
                 subreddit: Subreddit = None, link_id: str = ""):
        """
        Create a ``Listing`` instance.

        Parameters
        ----------
        reddit: Reddit
            The :class:`~apraw.Reddit` instance with which requests are made.
        data: Dict
            The data retrieved from the endpoint.
        kind_filter:
            Kinds to return if given, otherwise all are returned.
        subreddit: Subreddit
            The subreddit to inject into items as their owner.
        """
        super().__init__(reddit, data, reddit.listing_kind)

        self._index = 0
        self._subreddit = subreddit
        self._link_id = link_id
        self._kind_filter = kind_filter if kind_filter else []

    def __len__(self) -> int:
        """
        Return the number of items in the Listing.

        Returns
        -------
        len: int
            The number of items in the listing.
        """
        return len(getattr(self, self.CHILD_ATTRIBUTE))

    def __iter__(self) -> Iterator[aPRAWBase]:
        """
        Permit Listing to operate as an iterator.

        Returns
        -------
        self: Listing
            The iterator.
        """
        return self

    def __next__(self) -> aPRAWBase:
        """
        Permit Listing to operate as a generator.

        Returns
        -------
        item: aPRAWBase
            The next item in the listing.
        """
        while True:
            if self._index >= len(self):
                raise StopIteration()
            self._index += 1
            item = self[self._index - 1]

            if not self._kind_filter or (self._kind_filter and item.kind in self._kind_filter):
                break

        return item

    def __getitem__(self, index: int) -> aPRAWBase:
        """
        Return the item at position index in the list.

        Parameters
        ----------
        index : int
            The item's index.

        Returns
        -------
        item: aPRAWBase
            The searched item.
        """
        item = getattr(self, self.CHILD_ATTRIBUTE)[index]

        if isinstance(item, aPRAWBase):
            return item

        if "page" in item:
            return WikipageRevision(self._reddit, item)
        elif item["kind"] == self._reddit.link_kind:
            return Submission(self._reddit, item["data"], subreddit=self._subreddit)
        elif item["kind"] == self._reddit.subreddit_kind:
            return Subreddit(self._reddit, item["data"])
        elif item["kind"] == self._reddit.comment_kind:
            if item["data"]["replies"] and item["data"]["replies"]["kind"] == self._reddit.listing_kind:
                from ..helpers.comment_forest import CommentForest
                replies = CommentForest(self._reddit, item["data"]["replies"]["data"], item["data"]["link_id"])
            else:
                replies = []
            return Comment(self._reddit, item["data"], subreddit=self._subreddit, replies=replies)
        elif item["kind"] == self._reddit.modaction_kind:
            return ModAction(self._reddit, item["data"], self._subreddit)
        elif item["kind"] == self._reddit.message_kind:
            return Message(self._reddit, item["data"])
        elif item["kind"] == self._reddit.listing_kind:
            return Listing(self._reddit, item["data"])
        elif item["kind"] == self._reddit.more_kind:
            return MoreComments(self._reddit, item["data"], self._link_id)
        else:
            return aPRAWBase(self._reddit, item["data"] if "data" in item else item)

    @property
    def last(self) -> aPRAWBase:
        """
        Return the last item in the listing.

        Returns
        -------
        item: aPRAWBase
            The last item in the listing.
        """
        return self[len(self) - 1] if len(self) > 0 else None


class MoreChildren(Listing):
    CHILD_ATTRIBUTE = "things"
