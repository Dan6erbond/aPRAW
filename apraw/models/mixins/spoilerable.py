from ...const import API_PATH


class SpoilerableMixin:
    """
    Mixin for spoilerable objects.
    """

    async def mark_spoiler(self):
        """
        Mark the item as a spoiler.

        Returns
        -------
        resp: Dict
            The API response JSON.
        """
        return await self._reddit.post(API_PATH["post_spoiler"], id=self.fullname)

    async def unmark_spoiler(self):
        """
        Unmark the item as a spoiler.

        Returns
        -------
        resp: Dict
            The API response JSON.
        """
        return await self._reddit.post(API_PATH["post_unspoiler"], id=self.fullname)
