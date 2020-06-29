from enum import Enum
from typing import TYPE_CHECKING, NewType

from ...endpoints import API_PATH
from .apraw_base import aPRAWBase

if TYPE_CHECKING:
    from ...reddit import Reddit


class DistinguishmentOption(Enum):
    YES = "yes"
    NO = "no"
    ADMIN = "admin"
    SPECIAL = "special"


DISTINGUISHMENT_OPTIONS = NewType(
    "DistinguishmentOptions",
    DistinguishmentOption)


class ItemModeration:
    """
    A helper class to moderate comments, submissions and modmail.

    Members
    -------
    reddit: Reddit
        The :class:`~apraw.Reddit` instance with which requests are made.
    fullname: str
        The ID prepended with the kind of the item this helper belongs to.
    """

    def __init__(self, reddit: 'Reddit', item: aPRAWBase):
        """
        Create an instance of ``ItemModeration``.

        Parameters
        ----------
        reddit : Reddit
            The :class:`~apraw.Reddit` instance with which requests are made.
        item : aPRAWBase
            The item this helper performs requests for.
        """
        self.reddit = reddit
        self.fullname = item.fullname

    async def approve(self):
        """
        Approve the Reddit item.

        Returns
        -------
        resp: Dict
            The API response JSON.
        """
        return await self.reddit.post_request(API_PATH["mod_approve"], id=self.fullname)

    async def remove(self):
        """
        Remove the Reddit item.

        Returns
        -------
        resp: Dict
            The API response JSON.
        """
        return await self.reddit.post_request(API_PATH["mod_remove"], id=self.fullname)

    async def distinguish(self,
                          how: DISTINGUISHMENT_OPTIONS = "yes",
                          sticky: bool = False):
        """
        Distinguish the Reddit item.

        Parameters
        ----------
        how : "yes" or "no" or "admin" or "special"
            The type of distinguishment to be added to the item.
        sticky : bool, optional
            Whether the item should be stickied.

        Returns
        -------
        resp: Dict
            The API response JSON.
        """
        return await self.reddit.post_request(API_PATH["mod_distinguish"],
                                              id=self.fullname, how=how, sticky=sticky)

    async def undistinguish(self):
        """
        Undistinguish the Reddit item.

        Returns
        -------
        resp: Dict
            The API response JSON.
        """
        return await self.reddit.post_request(API_PATH["mod_distinguish"],
                                              id=self.fullname, how="no", sticky=False)

    async def ignore_reports(self):
        """
        Ignore reports on the Reddit item.

        Returns
        -------
        resp: Dict
            The API response JSON.
        """
        return await self.reddit.post_request(API_PATH["mod_ignore_reports"], id=self.fullname)

    async def unignore_reports(self):
        """
        Unignore previously ignored reports on the Reddit item.

        Returns
        -------
        resp: Dict
            The API response JSON.
        """
        return await self.reddit.post_request(API_PATH["mod_unignore_reports"], id=self.fullname)


class PostModeration(ItemModeration):
    """
    A helper class to moderate comments and submissions.

    Members
    -------
    reddit: Reddit
        The :class:`~apraw.Reddit` instance with which requests are made.
    fullname: str
        The ID prepended with the kind of the item this helper belongs to.
    """

    def __init__(self, reddit, item):
        """
        Create an instance of ``PostModeration``.

        Parameters
        ----------
        reddit : Reddit
            The :class:`~apraw.Reddit` instance with which requests are made.
        item : aPRAWBase
            The item this helper performs requests for.
        """
        super().__init__(reddit, item)

    async def lock(self):
        """
        Lock the item from further replies.

        Returns
        -------
        resp: Dict
            The API response JSON.
        """
        return await self.reddit.post_request(API_PATH["mod_lock"], id=self.fullname)

    async def unlock(self):
        """
        Unlock the item from further replies.

        Returns
        -------
        resp: Dict
            The API response JSON.
        """
        return await self.reddit.post_request(API_PATH["mod_unlock"], id=self.fullname)
