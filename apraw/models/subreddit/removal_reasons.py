from typing import TYPE_CHECKING, Dict, Optional, Any, Union

from ..helpers.apraw_base import aPRAWBase
from ...const import API_PATH

if TYPE_CHECKING:
    from .subreddit import Subreddit
    from ...reddit import Reddit


class SubredditRemovalReason(aPRAWBase):
    """
    The model representing subreddits.

    Members
    -------
    url: str
        The API URL to this specific removal reason.

    **Typical Attributes**

    This table describes attributes that typically belong to objects of this
    class. Attributes are dynamically provided by the :class:`~apraw.models.aPRAWBase` class
    and may vary depending on the status of the response and expected objects.

    =========== ============================================================
    Attribute   Description
    =========== ============================================================
    ``message`` The message for this removal reason that is sent to authors.
    ``id``      The ID of this removal reason.
    ``title``   The title of this removal reason in the subreddit.
    =========== ============================================================
    """

    def __init__(self, reddit: 'Reddit', subreddit: 'Subreddit', data: Dict):
        """
        Create an instance of a ``SubredditRemovalReason``.

        Parameters
        ----------
        reddit: Reddit
            The :class:`~apraw.Reddit` instance with which requests are made.
        subreddit: Subreddit
            The subreddit this helper operates under.
        data: Dict
            The data obtained from the /about endpoint.
        """
        super().__init__(reddit, data)
        self._subreddit = subreddit
        self.url = API_PATH["subreddit_removal_reason"].format(sub=self._subreddit.display_name, id=self.id)

    async def fetch(self):
        """
        Fetch the data for this removal reason. The :class:`~apraw.models.aPRAWBase` class will automatically update
        and/or add members returned by the API.
        """
        url = API_PATH["subreddit_removal_reasons"].format(sub=self._subreddit.display_name)
        res = await self._reddit.get(url)
        super()._update(res["data"][self.id])

    async def delete(self) -> Any:
        """
        Delete this removal reason from the subreddit.

        Returns
        -------
        response: Any
            The API endpoint raw response.
        """
        res = await self._reddit.delete(self.url)
        return res

    async def update(self, title: Optional[str] = None, message: Optional[str] = None) -> Any:
        """
        Update the title and/or message of this removal reason.

        Parameters
        ----------
        title: Optional[str]
            The updated title for this removal reason. If none is specified the original title will be reused.
        message: Optional[str]
            The updated message for this removal reason. If none is specified the original message will be reused.

        Returns
        -------
        response: Any
            The API endpoint raw response.
        """
        data = {
            k: v if v else getattr(self, k)
            for k, v in {"message": message, "title": title}.items()
        }
        await self._reddit.put(self.url, data=data)

    def __str__(self):
        """
        Retrieve a string representation of this removal reason.

        Returns
        -------
        id: str
            This removal reason's full ID.
        """
        return self.id


class SubredditRemovalReasons:
    """
    A helper to aid in retrieving and adding removal reasons to a subreddit.
    """

    def __init__(self, reddit: 'Reddit', subreddit: 'Subreddit'):
        """
        Create an instance of ``SubredditRemovalReasons``.

        Parameters
        ----------
        reddit: Reddit
            The reddit instance with which requests are made.
        subreddit: Subreddit
            The subreddit for which this helper performs requests.
        """
        self._reddit = reddit
        self._subreddit = subreddit
        self._removal_reasons = list()
        self._index = 0

    async def _fetch(self):
        """
        Refresh the data for the subreddit removal reasons.
        """
        url = API_PATH["subreddit_removal_reasons"].format(sub=self._subreddit.display_name)
        res = await self._reddit.get(url)

        for reason_id in res["order"]:
            reason = SubredditRemovalReason(self._reddit, self._subreddit, res["data"][reason_id])
            self._removal_reasons.append(reason)

    async def get(self, item: Union[int, str]) -> SubredditRemovalReason:
        """
        Retrieve a removal reason based on its ID or index.

        Parameters
        ----------
        item: int or str
            The item's ID or index.

        Returns
        -------
        reason: SubredditRemovalReason
            The removal reason that was found in the list.

        Raises
        ------
        StopIteration
            If no removal reason by the given ID was found.
        IndexError
            If the index given doesn't exist in the list of removal reasons.
        """
        if not self._removal_reasons:
            await self._fetch()

        if isinstance(item, str):
            return next(reason for reason in self._removal_reasons if reason.id == item)
        else:
            return self._removal_reasons[item]

    def __aiter__(self):
        """
        Permit ``SubredditRemovalReasons`` to operate as an iterator.

        Returns
        -------
        self: SubredditRemovalReasons
            The iterator.
        """
        return self

    async def __anext__(self):
        """
        Permit ``SubredditRemovalReason`` to operate as a generator.

        Returns the next removal reason in the listing.

        Returns
        -------
        reason: SubredditRemovalReason
            The next removal reason in the list.

        Raises
        ------
        StopAsyncIteration
            Raised once the list of removal reasons has been exhausted.
        """
        if not self._removal_reasons:
            await self._fetch()

        if self._index >= len(self._removal_reasons):
            raise StopAsyncIteration

        self._index += 1
        return self._removal_reasons[self._index - 1]

    async def add(self, title: str, message: str) -> SubredditRemovalReason:
        """
        Add a removal reason to the subreddit's list.

        Parameters
        ----------
        title: str
            The title under which this removal reason is saved.
        message: str
            The message that is sent to author's when the removal reason is used.

        Returns
        -------
        reason: SubredditRemovalReason
            The newly created, and fetched, removal reason.
        """
        data = {"message": message, "title": title}
        url = API_PATH["subreddit_removal_reasons"].format(sub=self._subreddit.display_name)

        data = await self._reddit.post(url, data=data)

        reason = SubredditRemovalReason(self._reddit, self._subreddit, data)
        await reason.fetch()
        return reason
