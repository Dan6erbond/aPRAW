from typing import TYPE_CHECKING, Dict, Iterator

from ..comment import Comment
from ..submission import Submission
from ..subreddit import ModAction, Subreddit
from ..subreddit_wiki import WikipageRevision
from .apraw_base import aPRAWBase

if TYPE_CHECKING:
    from ...reddit import Reddit


class Listing(aPRAWBase, Iterator):
    """
    A model representing Reddit listings.

    Members
    -------
    CHILD_ATTRIBUTE: str
        The attribute in the data that contains the listing's items.
    """

    CHILD_ATTRIBUTE = "children"

    def __init__(self, reddit: 'Reddit', data: Dict,
                 subreddit: Subreddit = None):
        super().__init__(reddit, data, reddit.listing_kind)

        self._index = 0
        self._subreddit = subreddit

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
        Permit ListingGenerator to operate as an iterator.

        Returns
        -------
        self: Listing
            The iterator.
        """
        return self

    def __next__(self) -> aPRAWBase:
        """
        Permit ListingGenerator to operate as a generator.

        Returns
        -------
        item: aPRAWBase
            The next item in the listing.
        """
        if self._index >= len(self):
            raise StopIteration()

        self._index += 1
        return self[self._index - 1]

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
        data = getattr(self, self.CHILD_ATTRIBUTE)[index]
        item = None

        if "page" in data:
            item = WikipageRevision(self.reddit, data)
        elif data["kind"] == self.reddit.link_kind:
            item = Submission(
                self.reddit,
                data["data"],
                subreddit=self._subreddit)
        elif data["kind"] == self.reddit.subreddit_kind:
            item = Subreddit(self.reddit, data["data"])
        elif data["kind"] == self.reddit.comment_kind:
            item = Comment(
                self.reddit,
                data["data"],
                subreddit=self._subreddit)
        elif data["kind"] == self.reddit.modaction_kind:
            item = ModAction(self.reddit, data["data"], self._subreddit)
        else:
            item = aPRAWBase(self.reddit,
                             data["data"] if "data" in data else data)

        return item

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
