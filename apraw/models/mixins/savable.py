from ...endpoints import API_PATH


class SavableMixin:
    """
    Mixin for savable objects.
    """

    async def save(self, category: str = ""):
        """
        Save the item in a category.

        Parameters
        ----------
        category : str, optional
            The category name.

        Returns
        -------
        resp: Dict
            The API response JSON.
        """
        return await self.reddit.post_request(API_PATH["post_save"], id=self.fullname, category=category)

    async def unsave(self):
        """
        Unsave the item.

        Returns
        -------
        resp: Dict
            The API response JSON.
        """
        return await self.reddit.post_request(API_PATH["post_unsave"], id=self.fullname)
