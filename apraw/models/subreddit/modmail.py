from typing import TYPE_CHECKING, Any, Dict, Optional

from ..helpers.apraw_base import aPRAWBase
from ...const import API_PATH

if TYPE_CHECKING:
    from .subreddit import Subreddit
    from ..reddit.redditor import Redditor
    from ...reddit import Reddit


class SubredditModmail:
    """
    Helper class to aid in retrieving subreddit modmail.
    """

    def __init__(self, reddit: 'Reddit', subreddit: 'Subreddit'):
        """
        Create an instance of SubredditModmail.

        Parameters
        ----------
        reddit: Reddit
            The :class:`~apraw.Reddit` instance with which requests are made.
        subreddit: Subreddit
            The subreddit this helper operates under.
        """
        self._reddit = reddit
        self._subreddit = subreddit

    async def __call__(self, id: str, mark_read=False) -> 'ModmailConversation':
        """
        Fetch a :class:`~apraw.models.ModmailConversation` by its ID.

        Parameters
        ----------
        id: str
            The conversation's ID.

        Returns
        -------
        conversation: ModmailConversation
            The conversation requested if it exists.
        """
        return await ModmailConversation(self._reddit, {"id": id}).fetch(mark_read)

    async def conversations(self) -> 'ModmailConversation':
        """
        Retrieve a list of modmail conversations.

        Yields
        ------
        conversation: ModmailConversation
            A modmail conversation held in the subreddit.
        """
        req = await self._reddit.get(API_PATH["modmail_conversations"],
                                     entity=self._subreddit.display_name)
        for _id in req["conversations"]:
            yield ModmailConversation(self._reddit, req["conversations"][_id])


class ModmailConversation(aPRAWBase):
    """
    The model for modmail conversations.

    **Typical Attributes**

    This table describes attributes that typically belong to objects of this
    class. Attributes are dynamically provided by the :class:`~apraw.models.aPRAWBase` class
    and may vary depending on the status of the response and expected objects.

    ==================== ==========================================================================================
    Attribute            Description
    ==================== ==========================================================================================
    ``authors``          A list of dictionaries containing authors by name with additional meta information such as
                         ``isMod``, ``isAdmin``, ``isOp``, ``isParticipant``, ``isHidden``, ``id``, ``isDeleted``.
    ``id``               The ID of this conversation.
    ``is_auto``          ``bool``
    ``is_highlighted``   Whether the conversation has been highlighted.
    ``is_internal``      Whether it's an internal mod conversation.
    ``is_repliable``     Whether the conversation can be replied to.
    ``last_mod_update``  A timestamp of the last moderator update or ``None``.
    ``last_unread``      ``None``
    ``last_updated``     A timestamp of the last update made overall.
    ``last_user_update`` A timestamp of the last user update or ``None``.
    ``num_messages``     The number of messages in this conversation.
    ``obj_ids``          A list of dictionaries containing the objects with their IDs and keys.
    ``owner``            A dictionary describing the subreddit this conversation is held in.
    ``participant``      ``Dict``
    ``state``            ``int``
    ``subject``          The subject of this conversation.
    ==================== ==========================================================================================

    """

    def __init__(self, reddit: 'Reddit', data: Dict,
                 owner: 'Subreddit' = None):
        """
        Create an instance of ``ModmailConversation``.

        Parameters
        ----------
        reddit: Reddit
            The :class:`~apraw.Reddit` instance with which requests are made.
        data: Dict
            The data obtained from the /about endpoint.
        owner: Subreddit
            The subreddit this conversation was held in.
        """
        super().__init__(reddit, data)
        self._owner = owner
        self._messages = list()

    async def fetch(self, mark_read=False):
        """
        Fetch this item's information from a suitable API endpoint.

        Returns
        -------
        self: ModmailConversation
            The updated model.
        """
        url = API_PATH["modmail_conversation"].format(id=self._data["id"])
        resp = await self._reddit.get(url, mark_read=mark_read)
        self._update(resp)
        return self

    def _update(self, data: Dict[str, Any]):
        """
        Update the base with new information.

        Parameters
        ----------
        data: Dict
            The data obtained from a suitable API endpoint.

        Returns
        -------
        self: ModmailConversation
            The updated model.
        """
        if isinstance(data, Dict):
            if "fields" in data:
                raise Exception(f"{data['message']}: {data['reason']}")
            _data = data.get("conversation", None) or data.get("conversations", None) or data
            super()._update(_data)
            if "messages" in data:
                self._messages = [ModmailMessage(self._reddit, data["messages"][msg_id], self) for msg_id in
                                  data["messages"]]
        else:
            raise Exception(f"Unexpected data: {data}")
        return self

    async def reply(self, body: str, author_hidden: bool = False, internal: bool = False):
        """
        Reply to the modmail conversation.

        Parameters
        ----------
        body: str
            The markdown reply body.
        author_hidden: bool
            Whether the author of this reply should be hidden.
        internal: bool
            Whether the reply is internal.

        Returns
        -------
        self: ModmailConversation
            The updated model.
        """
        url = API_PATH["modmail_conversation"].format(id=self._data["id"])
        resp = await self._reddit.post(url, data={
            "body": body,
            "conversation_id": self._data["id"],
            "isAuthorHidden": author_hidden,
            "isInternal": internal
        })
        return self._update(resp)

    async def _take_action(self, action: str, **kwargs):
        r"""
        Perform an action on the modmail conversation.

        Parameters
        ----------
        action: str
            The action to perform.
        kwargs: \*\*Dict
            Additional request data.

        Returns
        -------
        self: ModmailConversation
            The updated model.
        """
        url = API_PATH["modmail_conversation_action"].format(id=self._data["id"], action=action)
        resp = await self._reddit.post(url, **kwargs)
        return self._update(resp) if resp else self

    async def archive(self):
        """
        Archive the modmail conversation.

        Returns
        -------
        self: ModmailConversation
            The updated model.
        """
        return await self._take_action("archive")

    async def unarchive(self):
        """
        Unarchive the modmail conversation.

        Returns
        -------
        self: ModmailConversation
            The updated model.
        """
        return await self._take_action("unarchive")

    async def highlight(self):
        """
        Highlight the modmail conversation.

        Returns
        -------
        self: ModmailConversation
            The updated model.
        """
        return await self._take_action("highlight")

    async def remove_highlight(self):
        """
        Remove the highlight from the modmail conversation.

        Returns
        -------
        self: ModmailConversation
            The updated model.
        """
        url = API_PATH["modmail_conversation_action"].format(id=self._data["id"], action="higlight")
        resp = await self._reddit.delete(url)
        return self._update(resp) if resp else self

    async def mute(self):
        """
        Mute the modmail conversation.

        Returns
        -------
        self: ModmailConversation
            The updated model.
        """
        return await self._take_action("mute")

    async def unmute(self):
        """
        Unmute the modmail conversation.

        Returns
        -------
        self: ModmailConversation
            The updated model.
        """
        return await self._take_action("unmute")

    async def owner(self) -> 'Subreddit':
        """
        Retrieve the owner subreddit of this conversation.

        Returns
        -------
        owner: Subreddit
            The subreddit this conversation was held in.
        """
        if self._owner is None:
            self._owner = await self._reddit.subreddit(self._data["owner"]["displayName"])
        return self._owner

    async def messages(self) -> 'ModmailMessage':
        """
        Retrieve the messages sent in this conversation.

        Yields
        ------
        message: ModmailMessage
            A message sent in this conversation.
        """
        if not self._messages:
            await self.fetch()

        for msg in self._messages:
            yield msg


class ModmailMessage(aPRAWBase):
    """
    The model for modmail messages.

    Members
    -------
    conversation: ModmailConversation
        The :class:`~apraw.models.ModmailConversation` instance this message belongs to.

    **Typical Attributes**

    This table describes attributes that typically belong to objects of this
    class. Attributes are dynamically provided by the :class:`~apraw.models.aPRAWBase` class
    and may vary depending on the status of the response and expected objects.

    ==================== ==================================================
    Attribute            Description
    ==================== ==================================================
    ``id``               The ID of this message.
    ``body``             The HTML body of this message.
    ``body_markdown``    The raw body of this message.
    ``body_md``          An alias to ``body_markdown``.
    ``is_internal``      Whether the message was sent internally.
    ``date``             The datetime string on which the message was sent.
    ==================== ==================================================

    """

    def __init__(self, reddit: 'Reddit', data: Dict, conversation: ModmailConversation):
        """
        Create an instance of a modmail message.

        Parameters
        ----------
        conversation: ModmailConversation
            The :class:`~apraw.models.ModmailConversation` instance this message belongs to.
        data: Dict
            The data obtained from the API.
        """
        super().__init__(reddit, data)
        self.conversation = conversation
        self._author = None

    def _update(self, data: Dict[str, Any]):
        """
        Update the base with new information.

        Parameters
        ----------
        data: Dict
            The data obtained from a suitable API endpoint.

        Returns
        -------
        self: ModmailMessage
            The updated model.
        """
        data["body_md"] = data.get("bodyMarkdown", "")
        super()._update(data)

    async def author(self) -> Optional['Redditor']:
        """
        Retrieve the author of this message as a :class:`~apraw.models.Redditor`.

        Returns
        -------
        author: Redditor or None
            The author of this modmail message if they haven't been deleted yet.
        """
        if self._author is None:
            if not self._data["author"]["isDeleted"]:
                self._author = await self.conversation._reddit.redditor(self._data["author"]["name"])
            else:
                return None
        return self._author
