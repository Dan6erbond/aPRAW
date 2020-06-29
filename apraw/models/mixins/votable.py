from ...endpoints import API_PATH


class VotableMixin:
    """
    Mixin for votable objects.
    """

    async def upvote(self):
        """
        Upvote the item.

        Returns
        -------
        resp: Dict
            The API response JSON.
        """
        return await self.reddit.post_request(API_PATH["post_vote"], id=self.fullname, dir=1)

    async def downvote(self):
        """
        Downvote the item.

        Returns
        -------
        resp: Dict
            The API response JSON.
        """
        return await self.reddit.post_request(API_PATH["post_vote"], id=self.fullname, dir=-1)

    async def clear_vote(self):
        """
        Clear user up- and downvotes on the item.

        Returns
        -------
        resp: Dict
            The API response JSON.
        """
        return await self.reddit.post_request(API_PATH["post_vote"], id=self.fullname, dir=0)
