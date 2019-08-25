class SubredditModmail:
    def __init__(self, subreddit):
        self.subreddit = subreddit

    async def conversations(self):
        req = await self.subreddit.reddit.get_request("/api/mod/conversations", entity=self.subreddit.display_name)
        for id in req["conversations"]:
            yield ModmailConversation(self.subreddit.reddit, req["conversations"][id])


class ModmailConversation:
    def __init__(self, reddit, data, owner=None):
        self.reddit = reddit
        self.data = data
        self._data = None

        self.id = data["id"]
        self._owner = owner

        self.subject = data["subject"]

        self.is_auto = data["isAuto"]
        self.obj_ids = data["objIds"]
        self.is_repliable = data["isRepliable"]
        self.last_user_update = data["lastUserUpdate"]
        self.is_internal = data["isInternal"]
        self.lastModUpdate = data["lastModUpdate"]
        self.lastUpdated = data["lastUpdated"]
        self.is_highlighted = data["isHighlighted"]
        self.state = data["state"]
        self.last_unread = data["lastUnread"]
        self.num_messages = data["numMessages"]

        self.authors = data["authors"]
        self.participant = data["participant"]

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
            self._data = await self.reddit.get_request("/api/mod/conversations/{}".format(self.id))
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
                self._author = self.conversation.reddit.redditor(self.data["author"]["name"])
            else:
                return None
        return self._author