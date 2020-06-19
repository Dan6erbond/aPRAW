from datetime import datetime
from typing import TYPE_CHECKING, Dict

import aiohttp

from ..endpoints import API_PATH
from .redditor import Redditor

if TYPE_CHECKING:
    from ..reddit import Reddit


class User:

    def __init__(self, reddit: 'Reddit', username: str, password: str, client_id: str,
                 client_secret: str, user_agent: str):
        self.reddit = reddit

        self.username = username
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent

        if self.username == "" or self.password == "" or self.client_id == "" or self.client_secret == "":
            raise Exception(
                "No login information given or login information incomplete.")

        self.password_grant = "grant_type=password&username={}&password={}".format(
            self.username, self.password)

        self._auth_session = None
        self._client_session = None

        self._auth_user = None

        self.access_data = None
        self.token_expires = datetime.now()

        self.ratelimit_remaining = 0
        self.ratelimit_used = 0
        self.ratelimit_reset = datetime.now()

    def get_auth_session(self) -> aiohttp.ClientSession:
        if self._auth_session is None:
            auth = aiohttp.BasicAuth(
                login=self.client_id,
                password=self.client_secret)
            self._auth_session = aiohttp.ClientSession(auth=auth)
        return self._auth_session

    def get_client_session(self) -> aiohttp.ClientSession:
        if self._client_session is None:
            self._client_session = aiohttp.ClientSession()
        return self._client_session

    async def me(self) -> 'AuthenticatedUser':
        if not self._auth_user:
            data = await self.reddit.get_request(API_PATH["me"])
            self._auth_user = AuthenticatedUser(self.reddit, data)
        return self._auth_user


class AuthenticatedUser(Redditor):

    def __init__(self, reddit: 'Reddit', data: Dict):
        super().__init__(reddit, data)

        self._karma = None

    async def karma(self):
        if not self._karma:
            data = await self.reddit.get_request(API_PATH["me"])
            self._karma = AuthenticatedUser(self.reddit, data)
        return self._karma
