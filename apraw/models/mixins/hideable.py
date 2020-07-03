from ...endpoints import API_PATH


class HideableMixin:
    """
    Mixin for hideable objects.
    """

    async def hide(self):
        """
        Hide the item.

        Returns
        -------
        resp: Dict
            The API response JSON.
        """
        return await self.reddit.post_request(API_PATH["post_hide"], id=self.fullname)

    async def unhide(self):
        """
        Unhide the item.

        Returns
        -------
        resp: Dict
            The API response JSON.
        """
        return await self.reddit.post_request(API_PATH["post_unhide"], id=self.fullname)
