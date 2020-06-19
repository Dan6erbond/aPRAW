from typing import TYPE_CHECKING, Dict

from ..endpoints import API_PATH
from ..utils import snake_case_keys
from .apraw_base import aPRAWBase

if TYPE_CHECKING:
    from .subreddit import Subreddit
    from .redditor import Redditor
    from ..reddit import Reddit


class SubredditModmail:

    def __init__(self, subreddit: 'Subreddit'):
        self.subreddit = subreddit

    async def conversations(self) -> 'ModmailConversation':
        req = await self.subreddit.reddit.get_request(API_PATH["modmail_conversations"], entity=self.subreddit.display_name)
        for id in req["conversations"]:
            yield ModmailConversation(self.subreddit.reddit, req["conversations"][id])


class ModmailConversation(aPRAWBase):

    def __init__(self, reddit: 'Reddit', data: Dict,
                 owner: 'Subreddit' = None):
        super().__init__(reddit, data)

        self._data = None

        self.id = data["id"]
        self._owner = owner

    async def owner(self) -> 'Subreddit':
        if self._owner is None:
            self._owner = await self.reddit.subreddit(self.data["owner"]["displayName"])
        return self._owner

    async def messages(self) -> 'ModmailMessage':
        full_data = await self.full_data()
        for msg_id in full_data["messages"]:
            yield ModmailMessage(self, full_data["messages"][msg_id])

    async def full_data(self) -> Dict:
        if self._data is None:
            self._data = await self.reddit.get_request(API_PATH["modmail_conversation"].format(id=self.id))
        return self._data


class ModmailMessage:

    def __init__(self, conversation: ModmailConversation, data: Dict):
        self.conversation = conversation
        self.data = data

        self.id = data["id"]

        self.body = data["body"]
        self.body_md = data["bodyMarkdown"]
        self._author = None
        self.is_internal = data["isInternal"]
        self.date = data["date"]

    async def author(self) -> 'Redditor':
        if self._author is None:
            if not self.data["author"]["isDeleted"]:
                self._author = self.conversation.reddit.redditor(
                    self.data["author"]["name"])
            else:
                return None
        return self._author
