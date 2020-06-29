from ...endpoints import API_PATH


class NSFWableMixin:
    """
    Mixin for NSFWable objects.
    """

    async def mark_nsfw(self):
        """
        Mark the item as NSFW.

        Returns
        -------
        resp: Dict
            The API response JSON.
        """
        return await self.reddit.post_request(API_PATH["post_marknsfw"], id=self.fullname)

    async def unmark_nsfw(self):
        """
        Unmark the item as NSFW.

        Returns
        -------
        resp: Dict
            The API response JSON.
        """
        return await self.reddit.post_request(API_PATH["post_unmarknsfw"], id=self.fullname)
