from ..endpoints import API_PATH
from ..utils import snake_case_keys


class SubredditModmail:
    def __init__(self, subreddit):
        self.subreddit = subreddit

    async def conversations(self):
        req = await self.subreddit.reddit.get_request(API_PATH["modmail_conversations"], entity=self.subreddit.display_name)
        for id in req["conversations"]:
            yield ModmailConversation(self.subreddit.reddit, req["conversations"][id])


class ModmailConversation:
    def __init__(self, reddit, data, owner=None):
        self.reddit = reddit
        self.data = data
        self._data = None

        self.id = data["id"]
        self._owner = owner

        ignore = ["owner"]
        d = snake_case_keys(data)
        for key in d:
            if not hasattr(self, key) and key not in ignore:
                setattr(self, key, d[key])

    async def owner(self):
        if self._owner is None:
            self._owner = await self.reddit.subreddit(self.data["owner"]["displayName"])
        return self._owner

    async def messages(self):
        full_data = await self.full_data()
        for msg_id in full_data["messages"]:
            yield ModmailMessage(self, full_data["messages"][msg_id])

    async def full_data(self):
        if self._data is None:
            self._data = await self.reddit.get_request(API_PATH["modmail_conversation"].format(id=self.id))
        return self._data


class ModmailMessage:
    def __init__(self, conversation, data):
        self.conversation = conversation
        self.data = data

        self.id = data["id"]

        self.body = data["body"]
        self.body_md = data["bodyMarkdown"]
        self._author = None
        self.is_internal = data["isInternal"]
        self.date = data["date"]

    async def author(self):
        if self._author is None:
            if not self.data["author"]["isDeleted"]:
                self._author = self.conversation.reddit.redditor(
                    self.data["author"]["name"])
            else:
                return None
        return self._author
