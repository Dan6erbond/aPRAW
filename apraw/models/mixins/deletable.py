from ...const import API_PATH


class DeletableMixin:
    """
    Mixin for deletable objects.
    """

    async def delete(self):
        """
        Delete the item.

        Returns
        -------
        resp: Dict
            The API response JSON.
        """
        return await self._reddit.post(API_PATH["post_delete"], id=self.fullname)
