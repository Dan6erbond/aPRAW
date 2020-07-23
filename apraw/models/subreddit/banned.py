from datetime import datetime
from typing import TYPE_CHECKING, Union, Optional, Dict

from ..helpers.apraw_base import aPRAWBase
from ..helpers.generator import ListingGenerator
from ..helpers.streamable import streamable
from ..mixins.redditor import RedditorMixin
from ..reddit.listing import Listing
from ..reddit.redditor import Redditor
from ...const import API_PATH

if TYPE_CHECKING:
    from ...reddit import Reddit
    from .subreddit import Subreddit


class BannedUser(aPRAWBase, RedditorMixin):
    """
    The model representing banned users on a subreddit. The Redditor can be retrieved via :meth:`~apraw.models.BannedUser.redditor()`.

    **Typical Attributes**

    This table describes attributes that typically belong to objects of this
    class. Attributes are dynamically provided by the :class:`~apraw.models.aPRAWBase` class
    and may vary depending on the status of the response and expected objects.

    ========================== ========================================================
    Attribute                  Description
    ========================== ========================================================
    ``banned``                 The parsed UTC date on which the user was banned.
    ``date``                   The UTC timestamp on which the user was banned.
    ``days_left``              The number of days left for the ban. ``0`` if permanent.
    ``id``                     The Redditor's fullname (t2_ID).
    ``name``                   The Redditor's name.
    ``note``                   The ban note added by the subreddit moderators.
    ``rel_id``                 ``str``
    ========================== ========================================================

    """

    def __init__(self, reddit: 'Reddit', data: Dict, subreddit: 'Subreddit'):
        """
        Create a BannedUser instance.

        Parameters
        ----------
        reddit: Reddit
            The :class:`~apraw.Reddit` instance with which requests are made.
        data: Dict
            The data obtained from the API.
        """
        if "date" in data:
            data["banned"] = datetime.utcfromtimestamp(data["date"])
        super().__init__(reddit, data, reddit.account_kind)
        self._subreddit = subreddit


class BannedListing(Listing):
    """
    A model representing listings of banned users.
    """

    def __getitem__(self, index: int) -> BannedUser:
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
        else:
            return BannedUser(self._reddit, item, self._subreddit)


class SubredditBanned:
    """
    A helper class for interacting with a subreddit's banned users.

    """

    def __init__(self, reddit: 'Reddit', subreddit: 'Subreddit'):
        """
        Create an instance of ``SubredditBanned``.

        Parameters
        ----------
        reddit: Reddit
            The :class:`~apraw.Reddit` instance with which requests are made.
        subreddit: Subreddit
            The subreddit this helper instance belongs to and performs requests for.
        """
        self._reddit = reddit
        self._subreddit = subreddit

    #: Streamable listing endpoint.
    @streamable
    async def __call__(self, redditor: Optional[Union[str, Redditor]] = None, limit: int = 100, **kwargs):
        r"""
        Returns an instance of :class:`~apraw.models.ListingGenerator` mapped to the subreddit's banned users.

        .. note::
            This listing can be streamed doing the following:

            .. code-block:: python3

                for comment in subreddit.banned.stream():
                    print(comment)

        Parameters
        ----------
        redditor: Redditor or str
            A single Redditor to search for, useful for checking if they have already been banned.
        kwargs: \*\*Dict
            :class:`~apraw.models.ListingGenerator` ``kwargs``.

        Returns
        -------
        generator: ListingGenerator
            A :class:`~apraw.models.ListingGenerator` mapped to the subreddit's banned users.
        """
        url = API_PATH["subreddit_banned"].format(sub=self._subreddit.display_name)
        if redditor:
            kwargs["redditor"] = str(redditor)
        return ListingGenerator(self._reddit, url, limit, self._subreddit, listing_class=BannedListing, **kwargs)

    async def add(self, redditor: Union[str, Redditor], **kwargs):
        r"""
        Ban a Reddit in the respective subreddit.

        Parameters
        ----------
        redditor: Redditor or str
            The Redditor to be banned.
        duration: int
            An optional duration if the ban is not permanent.
        ban_context: str
            Fullname of a thing to be used as the context.
        ban_message: str
            The message to be sent to the banned Redditor.
        ban_reason: str
            An additional reason for the ban.
        note: str
            An internal mod note.

        Returns
        -------
        resp: Dict
            The raw response JSON dictionary.
        """
        url = API_PATH["sub_friend"].format(sub=self._subreddit.display_name)
        data = {"name": str(redditor), "type": "banned"}
        data.update(**kwargs)
        return await self._reddit.post(url, data=data)

    async def remove(self, redditor: Union[str, Redditor]):
        """
        Unban a Reddit in the respective subreddit.

        Parameters
        ----------
        redditor: Redditor or str
            The Redditor to be banned.

        Returns
        -------
        resp: Dict
            The raw response JSON dictionary.
        """
        url = API_PATH["sub_unfriend"].format(sub=self._subreddit.display_name)
        return await self._reddit.post(url, data={"name": str(redditor), "type": "banned"})
