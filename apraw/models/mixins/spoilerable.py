from ...endpoints import API_PATH


class SpoilerableMixin:
    """
    Mixin for spoilerable objects.
    """

    async def spoiler(self):
        """
        Mark the item as a spoiler.

        Returns
        -------
        resp: Dict
            The API response JSON.
        """
        return await self.reddit.post_request(API_PATH["post_spoiler"], id=self.fullname)

    async def unspoiler(self):
        """
        Unmark the item as a spoiler.

        Returns
        -------
        resp: Dict
            The API response JSON.
        """
        return await self.reddit.post_request(API_PATH["post_unspoiler"], id=self.fullname)
