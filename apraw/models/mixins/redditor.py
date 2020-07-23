from ..reddit.redditor import Redditor


class RedditorMixin:
    """
    Mixin for items that represent a slimmed version of a Redditor.
    """

    def __str__(self):
        """
        Returns the Redditor's name.

        Returns
        -------
        name: str
            The Redditor's name.
        """
        return getattr(self, "name")

    async def redditor(self) -> Redditor:
        """
        Retrieve the Redditor this Moderator represents.

        Returns
        -------
        redditor: Redditor
            The Redditor that is represented by this object.
        """
        return await self._reddit.redditor(getattr(self, "name"))
