from ...endpoints import API_PATH
from ..redditor import Redditor


class AuthorMixin:
    """
    Mixin for items with an author.
    """

    def __init__(self, author: Redditor = None):
        self._author = author

    async def author(self) -> Redditor:
        """
        Retrieve the item's author as a :class:`~apraw.models.Redditor`.

        Returns
        -------
        author: Redditor
            The item's author.
        """
        if self._author is None:
            self._author = await self.reddit.redditor(self.data["author"])
        return self._author
