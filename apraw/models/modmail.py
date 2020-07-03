from typing import TYPE_CHECKING, Dict

from ..endpoints import API_PATH
from .helpers.apraw_base import aPRAWBase

if TYPE_CHECKING:
    from .subreddit import Subreddit
    from .redditor import Redditor
    from ..reddit import Reddit


class SubredditModmail:
    """
    Helper class to aid in retrieving subreddit modmail.

    Members
    -------
    subreddit: Subreddit
        The subreddit this helper operates under.
    """

    def __init__(self, subreddit: 'Subreddit'):
        """
        Create an instance of SubredditModmail.

        Parameters
        ----------
        subreddit: Subreddit
            The subreddit this helper operates under.
        """
        self.subreddit = subreddit

    async def conversations(self) -> 'ModmailConversation':
        """
        Retrieve a list of modmail conversations.

        Yields
        ------
        conversation: ModmailConversation
            A modmail conversation held in the subreddit.
        """
        req = await self.subreddit.reddit.get_request(API_PATH["modmail_conversations"],
                                                      entity=self.subreddit.display_name)
        for id in req["conversations"]:
            yield ModmailConversation(self.subreddit.reddit, req["conversations"][id])


class ModmailConversation(aPRAWBase):
    """
    The model for modmail conversations.

    Members
    -------
    reddit: Reddit
        The :class:`~apraw.Reddit` instance with which requests are made.
    data: Dict
        The data obtained from the /about endpoint.

    **Typical Attributes**

    This table describes attributes that typically belong to objects of this
    class. Attributes are dynamically provided by the :class:`~apraw.models.aPRAWBase` class
    and may vary depending on the status of the response and expected objects.

    ================== ==========================================================================================
    Attribute          Description
    ================== ==========================================================================================
    ``isAuto``         ``bool``
    ``objIds``         A list of dictionaries containing the objects with their IDs and keys.
    ``isRepliable``    Whether the conversation can be replied to.
    ``lastUserUpdate`` A timestamp of the last user update or ``None``.
    ``isInternal``     Whether it's an internal mod conversation.
    ``lastModUpdate``  A timestamp of the last moderator update or ``None``.
    ``lastUpdated``    A timestamp of the last update made overall.
    ``authors``        A list of dictionaries containing authors by name with additional meta information such as
                       ``isMod``, ``isAdmin``, ``isOp``, ``isParticipant``, ``isHidden``, ``id``, ``isDeleted``.
    ``owner``          A dictionary describing the subreddit this conversation is held in.
    ``id``             The ID of this conversation.
    ``isHighlighted``  Whether the conversation has been highlighted.
    ``subject``        The subject of this conversation.
    ``participant``    ``Dict``
    ``state``          ``int``
    ``lastUnread``     ``None``
    ``numMessages``    The number of messages in this conversation.
    ================== ==========================================================================================
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

        self._data = None
        self._owner = owner

    async def owner(self) -> 'Subreddit':
        """
        Retrieve the owner subreddit of this conversation.

        Returns
        -------
        owner: Subreddit
            The subreddit this conversation was held in.
        """
        if self._owner is None:
            self._owner = await self.reddit.subreddit(self.data["owner"]["displayName"])
        return self._owner

    async def messages(self) -> 'ModmailMessage':
        """
        Retrieve the messages sent in this conversation.

        Yields
        ------
        message: ModmailMessage
            A message sent in this conversation.
        """
        full_data = await self.full_data()
        for msg_id in full_data["messages"]:
            yield ModmailMessage(self, full_data["messages"][msg_id])

    async def full_data(self) -> Dict:
        """
        Retrieve the raw full data from the ``/api/mod/conversations/{id}`` endpoint.

        Returns
        -------
        full_data: Dict
            The full data retrieved from the endpoint.
        """
        if self._data is None:
            self._data = await self.reddit.get_request(API_PATH["modmail_conversation"].format(id=self.id))
        return self._data


class ModmailMessage:
    """
    The model for modmail messages.

    Members
    -------
    conversation: ModmailConversation
        The :class:`~apraw.models.ModmailConversation` instance this message belongs to.
    data: Dict
        The data obtained from the API.
    id: str
        The ID of this message.
    body: str
        The HTML body of this message.
    body_md: str
        The raw body of this message.
    is_internal: str
        Whether the message was sent internally.
    date: str
        A timestamp on which the message was sent.

    .. note::
        ``ModmailMessage`` attributes are loaded statically, meaning they will always be present under the
        abovementioned names.

    """

    def __init__(self, conversation: ModmailConversation, data: Dict):
        """
        Create an instance of a modmail message.

        Parameters
        ----------
        conversation: ModmailConversation
            The :class:`~apraw.models.ModmailConversation` instance this message belongs to.
        data: Dict
            The data obtained from the API.
        """
        self.conversation = conversation
        self.data = data

        self.id = data["id"]

        self.body = data["body"]
        self.body_md = data["bodyMarkdown"]
        self._author = None
        self.is_internal = data["isInternal"]
        self.date = data["date"]

    async def author(self) -> 'Redditor':
        """
        Retrieve the author of this message as a :class:`~apraw.models.Redditor`.

        Returns
        -------
        author: Redditor
            The author of this modmail message.
        """
        if self._author is None:
            if not self.data["author"]["isDeleted"]:
                self._author = self.conversation.reddit.redditor(  # TODO: Add 'await'
                    self.data["author"]["name"])
            else:
                return None
        return self._author
