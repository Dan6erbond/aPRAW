from ..reddit.submission import Submission


class LinkMixin:
    """
    Mixin for items belonging to a link / submission.
    """

    def __init__(self, link: Submission = None):
        self._link = link

    async def link(self) -> Submission:
        """
        Retrieve the item's author as a :class:`~apraw.models.Submission`.

        Returns
        -------
        link: Submission
            The item's parent link / submission.
        """
        if self._link is None:
            self._link = await self._reddit.redditor(getattr(self, "link_id"))
        return self._link

    submission = link
