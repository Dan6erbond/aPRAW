from datetime import datetime
from typing import TYPE_CHECKING, Dict, List

import aiohttp

from ..endpoints import API_PATH
from .helpers.apraw_base import aPRAWBase
from .redditor import Redditor

if TYPE_CHECKING:
    from ..reddit import Reddit


class User:
    """
    A class to store the authentication credentials and handle ratelimit information.

    Members
    -------
    reddit: Reddit
        The :class:`~apraw.Reddit` instance with which requests are made.
    username: str
        The username given to the Reddit instance or obtained via ``praw.ini``.
    password: str
        The password given to the Reddit instance or obtained via ``praw.ini``.
    client_id: str
        The client ID given to the Reddit instance or obtained via ``praw.ini``.
    client_secret: str
        The client secret given to the Reddit instance or obtained via ``praw.ini``.
    user_agent: str
        The user agent given to the Reddit instance or defaulted to aPRAW's version.
    password_grant: str
        The data to be used when making a token request with the 'password' ``grant_type``.
    access_data: Dict
        A dictionary containing the access token and user agent for request headers.
    token_expires: datetime
        The datetime on which the previously retrieved token will expire. Defaults to the past to obtain a token
        immediately the first time.
    ratelimit_remaining: int
        The number of requests remaining in the current ratelimit window.
    ratelimit_used: int
        The number of requests previously used in the current ratelimit window.
    ratelimit_reset: datetime
        The datetime on which the ratelimit window will be reset.
    """

    def __init__(self, reddit: 'Reddit', username: str, password: str, client_id: str,
                 client_secret: str, user_agent: str):
        """
        Create an instance of the authenticated user.

        Parameters
        ----------
        reddit: Reddit
            The :class:`~apraw.Reddit` instance with which requests are made.
        username: str
            The username given to the Reddit instance or obtained via ``praw.ini``.
        password: str
            The password given to the Reddit instance or obtained via ``praw.ini``.
        client_id: str
            The client ID given to the Reddit instance or obtained via ``praw.ini``.
        client_secret: str
            The client secret given to the Reddit instance or obtained via ``praw.ini``.
        user_agent: str
            The user agent given to the Reddit instance or defaulted to aPRAW's version.

        Raises
        ------
        Exception
            If the login credentials given are empty or incomplete.
        """
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
        """
        Retrieve an ``aiohttp.ClientSesssion`` with which the authentication token can be obtained.

        Returns
        -------
        session: aiohttp.ClientSession
            The session using the BasicAuth setup to obtain tokens with.
        """
        if self._auth_session is None:
            auth = aiohttp.BasicAuth(
                login=self.client_id,
                password=self.client_secret)
            self._auth_session = aiohttp.ClientSession(auth=auth)
        return self._auth_session

    def get_client_session(self) -> aiohttp.ClientSession:
        """
        Retrieve the ``aiohttp.ClientSesssion`` with which regular requests are made.

        Returns
        -------
        session: aiohttp.ClientSession
            The session with which requests should be made.
        """
        if self._client_session is None:
            self._client_session = aiohttp.ClientSession()
        return self._client_session

    async def me(self) -> 'AuthenticatedUser':
        """
        Retrieve an instance of :class:`~apraw.models.AuthenticatedUser` for the logged-in user.

        Returns
        -------
        user: AuthenticatedUser
            The logged-in user.
        """
        if not self._auth_user:
            data = await self.reddit.get_request(API_PATH["me"])
            self._auth_user = AuthenticatedUser(self.reddit, data)
        return self._auth_user


class AuthenticatedUser(Redditor):
    """
    The model representing the logged-in user.

    This model inherits from :class:`~apraw.models.Redditor` and thus all its attributes and features. View those docs
    for further information.

    Members
    -------
    reddit: Reddit
        The :class:`~apraw.Reddit` instance with which requests are made.
    data: Dict
        The data obtained from the /about endpoint.
    """

    def __init__(self, reddit: 'Reddit', data: Dict):
        """
        Create an instance of AuthenticatedUser.

        Parameters
        ----------
        reddit : Reddit
            The :class:`~apraw.Reddit` instance with which requests are made.
        data : Dict
            The data obtained from the /about endpoint.
        """
        super().__init__(reddit, data)

        self._karma = list()

    async def karma(self) -> List['Karma']:
        """
        Retrieve the karma breakdown for the logged-in user.

        Returns
        -------
        karma: List[Karma]
            The parsed ``KarmaList`` for the logged-in user.
        """
        if not self._karma:
            resp = await self.reddit.get_request(API_PATH["me_karma"])
            self._karma = [Karma(self.reddit, d) for d in resp["data"]]
        return self._karma


class Karma(aPRAWBase):
    """
    A model representing subreddit karma.

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

    ================= ===================================================
    Attribute         Description
    ================= ===================================================
    ``sr``            The name of the subreddit the karma was obtained on
    ``comment_karma`` The amount of karma obtained on the subreddit.
    ``link_karma``    The amount of link karma obtained on the subreddit.
    ================= ===================================================
    """

    def __init__(self, reddit: 'Reddit', data: Dict):
        """
        Create an instance of Karma

        Parameters
        ----------
        reddit : Reddit
            An instance of :class:`~apraw.Reddit`with which requests are made.
        data : Dict
            The data obtained from the /about endpoint.
        """
        super().__init__(reddit, data)

        self._subreddit = None

    async def subreddit(self):
        """
        Retrieve the subreddit on which the karma was obtained.

        Returns
        -------
        subreddit: Subreddit
            The subreddit on which the karma was obtained.
        """
        return await self.reddit.subreddit(self.sr)
