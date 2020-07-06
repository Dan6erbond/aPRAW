from typing import TYPE_CHECKING, Union

from ...endpoints import API_PATH

if TYPE_CHECKING:
    from ..reddit.message import Message
    from ..reddit.comment import Comment


class ReplyableMixin:
    """
    Mixin for replyable objects.
    """

    async def reply(self, text: str) -> Union['Comment', 'Message']:
        """
        Reply to the item.

        Returns
        -------
        reply: Comment or Message
            The newly created reply, either a :class:`~apraw.models.Comment` or :class:`~apraw.models.Message`.
        """
        resp = await self._reddit.post_request(API_PATH["reply"], text=text, return_rtjson=True, thing_id=self.fullname)

        if self.kind == self._reddit.message_kind:
            from ..reddit.message import Message
            reply = Message(self._reddit, resp)
        else:
            from ..reddit.comment import Comment
            reply = Comment(self._reddit, resp)

        return reply

    comment = reply
