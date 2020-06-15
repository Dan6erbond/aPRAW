from datetime import datetime

from ..endpoints import API_PATH
from .redditor import Redditor


class User:

    def __init__(self, reddit, username, password, client_id,
                 client_secret, user_agent):
        self.reddit = reddit

        self.username = username
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent

        if self.username == "" or self.password == "" or self.client_id == "" or self.client_secret == "":
            raise Exception(
                "No login information given or login information incomplete.")

        self._auth_user = None

        self.access_data = None
        self.token_expires = datetime.now()

        self.ratelimit_remaining = 0
        self.ratelimit_used = 0
        self.ratelimit_reset = datetime.now()

    async def me(self):
        if not self._auth_user:
            data = await self.reddit.get_request(API_PATH["me"])
            self._auth_user = AuthenticatedUser(self.reddit, data)
        return self._auth_user

class AuthenticatedUser(Redditor):

    def __init__(self, reddit, data):
        super().__init__(reddit, data)

        self._karma = None

    async def karma(self):
        if not self._karma:
            data = await self.reddit.get_request(API_PATH["me"])
            self._karma = AuthenticatedUser(self.reddit, data)
        return self._karma
