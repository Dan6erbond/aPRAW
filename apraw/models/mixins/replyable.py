from ...endpoints import API_PATH


class ReplyableMixin:
    """
    Mixin for replyable objects.
    """

    async def reply(self, text: str):
        """
        Reply to the item.

        Returns
        -------
        resp: Dict
            The API response JSON.
        """
        return await self.reddit.post_request(API_PATH["reply"], text=text, return_rtjson=True, thing_id=self.fullname)

    comment = reply
