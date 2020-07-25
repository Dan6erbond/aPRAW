import json
from typing import TYPE_CHECKING, Optional, Union

from .apraw_base import aPRAWBase
from ..enums.distinguishment_option import DistinguishmentOption
from ..subreddit.removal_reasons import SubredditRemovalReason
from ...const import API_PATH

if TYPE_CHECKING:
    from ...reddit import Reddit


class ItemModeration:
    """
    A helper class to moderate comments, submissions and modmail.
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
        self._reddit = reddit
        self._item = item

    async def approve(self):
        """
        Approve the Reddit item.

        Returns
        -------
        resp: Dict
            The API response JSON.
        """
        return await self._reddit.post(API_PATH["mod_approve"], id=self.fullname)

    async def _add_removal_reason(self, mod_note: Optional[str] = "", reason: Union[str, SubredditRemovalReason] = None):
        """
        Add a removal reason to a comment or submission.

        It is necessary to first call :meth:`~.remove` on the :class:`~.Comment` or :class:`~.Submission`.
        If ``reason_id`` is not specified, ``mod_note`` cannot be blank.

        Parameters
        ----------
        mod_note: Optional[str]
            A message for the other moderators.
        reason:  str or SubredditRemovalReason
            The removal reason ID or a subreddit removal reason to add.

        Returns
        -------
        resp: Dict
            The API response JSON.
        """
        if not reason and not mod_note:
            raise ValueError("mod_note cannot be blank if reason_id is not specified")
        # Only the first element of the item_id list is used.
        data = {
            "item_ids": [self.fullname],
            "mod_note": mod_note,
            "reason_id": str(reason),
        }
        return await self._reddit.post(API_PATH["removal_reasons"], data={"json": json.dumps(data)})

    async def remove(self, spam: bool = False, mod_note: Optional[str] = "",
                     reason: Union[str, SubredditRemovalReason] = None):
        """
        Remove the Reddit item.

        Parameters
        ----------
        spam: bool
            When ``True``, use the removal to help train the Subreddit's spam filter (default: ``False``).
        mod_note: Optional[str]
            A message for the other moderators.
        reason:  str or SubredditRemovalReason
            The removal reason ID or a subreddit removal reason to add.

        Returns
        -------
        resp: Dict or Tuple
            The API response JSON or a tuple of dictionaries if a removal reason / mod note was added as well.
        """
        data = {"id": self.fullname, "spam": bool(spam)}
        res = await self._reddit.post(API_PATH["mod_remove"], data=data)

        if any([reason, mod_note]):
            res1 = await self._add_removal_reason(mod_note, reason)
            return res, res1

        return res

    async def distinguish(self, how: DistinguishmentOption = "yes", sticky: bool = False):
        """
        Distinguish the Reddit item.

        Parameters
        ----------
        how : DistinguishmentOption
            The type of distinguishment to be added to the item.
        sticky : bool, optional
            Whether the item should be stickied.

        Returns
        -------
        resp: Dict
            The API response JSON.
        """
        return await self._reddit.post(API_PATH["mod_distinguish"], id=self.fullname, how=how, sticky=sticky)

    async def undistinguish(self):
        """
        Undistinguish the Reddit item.

        Returns
        -------
        resp: Dict
            The API response JSON.
        """
        return await self._reddit.post(API_PATH["mod_distinguish"], id=self.fullname, how="no", sticky=False)

    async def ignore_reports(self):
        """
        Ignore reports on the Reddit item.

        Returns
        -------
        resp: Dict
            The API response JSON.
        """
        return await self._reddit.post(API_PATH["mod_ignore_reports"], id=self.fullname)

    async def unignore_reports(self):
        """
        Unignore previously ignored reports on the Reddit item.

        Returns
        -------
        resp: Dict
            The API response JSON.
        """
        return await self._reddit.post(API_PATH["mod_unignore_reports"], id=self.fullname)

    @property
    def fullname(self) -> str:
        """
        Retrieve the fullname of the item this helper performs requests for.

        Returns
        -------
        fullname: str
            The ID prepended with the kind of the item this helper belongs to.
        """
        return self._item.fullname


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

    async def lock(self):
        """
        Lock the item from further replies.

        Returns
        -------
        resp: Dict
            The API response JSON.
        """
        return await self._reddit.post(API_PATH["mod_lock"], id=self.fullname)

    async def unlock(self):
        """
        Unlock the item from further replies.

        Returns
        -------
        resp: Dict
            The API response JSON.
        """
        return await self._reddit.post(API_PATH["mod_unlock"], id=self.fullname)
