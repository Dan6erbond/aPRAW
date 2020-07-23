from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..reddit.submission import Submission


class LinkMixin:
    """
    Mixin for items belonging to a submission.
    """

    def __init__(self, link: 'Submission' = None):
        self._link = link

    async def link(self) -> 'Submission':
        """
        Retrieve the submission this item belongs to as a :class:`~apraw.models.Submission`.

        Returns
        -------
        submission: Submission
            The item's parent submission.
        """
        if self._link is None:
            self._link = await self._reddit.submission(getattr(self, "link_id"))
        return self._link

    submission = link
