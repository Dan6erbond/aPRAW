import os
import asyncio
import configparser
import logging
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Awaitable, Callable, Dict, List, Union

from multidict import CIMultiDictProxy

from .endpoints import API_PATH, BASE_URL
from .models import (Comment, Listing, Redditor, Submission,
                     Subreddit, User, ListingGenerator, streamable)
from .utils import prepend_kind

if os.path.exists('praw.ini'):
    _prawfile = os.path.abspath('praw.ini')
elif 'APPDATA' in os.environ:  # Windows
    _prawfile = os.path.join(os.environ['APPDATA'], 'praw.ini')
elif 'XDG_CONFIG_HOME' in os.environ:  # Modern Linux
    _prawfile = os.path.join(os.environ['XDG_CONFIG_HOME'], 'praw.ini')
elif 'HOME' in os.environ:  # Legacy Linux
    _prawfile = os.path.join(os.environ['HOME'], '.config', 'praw.ini')


class Reddit:
    """
    The Reddit instance with which root requests can be made.

    Members
    -------
    user: User
        An instance of the logged-in Reddit user.
    """

    def __init__(self, praw_key: str = "", username: str = "", password: str = "",
                 client_id: str = "", client_secret: str = "",
                 user_agent="aPRAW by Dan6erbond"):
        """
        Create a Reddit instance.

        Parameters
        ----------
        praw_key: str
            The key used in a `praw.ini` file instead of manual username, password, client_id and secret.
        username: str
            The Reddit account username.
        password: str
            The Reddit account password.
        client_id: str
            The Reddit script's client_id.
        client_secret
            The Reddit script's client_secret.
        user_agent: str
            User agent to be used in the headers, defaults to "aPRAW by Dan6erbond".
        """
        if praw_key != "":
            config = configparser.ConfigParser()
            config.read(_prawfile)

            self.user = User(self, config[praw_key]["username"], config[praw_key]["password"],
                             config[praw_key]["client_id"], config[praw_key]["client_secret"],
                             config[praw_key]["user_agent"] if "user_agent" in config[praw_key] else user_agent)
        else:
            self.user = User(self, username, password,
                             client_id, client_secret, user_agent)

        self.comment_kind = "t1"
        self.account_kind = "t2"
        self.link_kind = "t3"
        self.message_kind = "t4"
        self.subreddit_kind = "t5"
        self.award_kind = "t6"
        self.modaction_kind = "modaction"
        self.listing_kind = "Listing"
        self.wiki_revision_kind = "WikiRevision"
        self.wikipage_kind = "wikipage"
        self.more_kind = "more"

        self.loop = asyncio.get_event_loop()
        self.request_handler = RequestHandler(self.user)

    @streamable
    def subreddits(self, *args, **kwargs):
        r"""
        A :class:`~apraw.models.ListingGenerator` that returns newly created subreddits, which can be streamed using :code:`reddit.subreddits.stream()`.

        Parameters
        ----------
        kwargs: \*\*Dict
            :class:`~apraw.models.ListingGenerator` ``kwargs``.

        Returns
        -------
        generator: ListingGenerator
            A :class:`~apraw.models.ListingGenerator` that retrieves newly created subreddits.
        """
        return ListingGenerator(self, API_PATH["subreddits_new"], *args, **kwargs)

    async def get_request(self, *args, **kwargs):
        """
        Perform an HTTP GET request on the Reddit API.

        Parameters
        ----------
        endpoint: str
            The endpoint to be appended after the base URL (https://oauth.reddit.com/).
        kwargs:
            Query parameters to be appended after the URL.

        Returns
        -------
        resp: Dict or None
            The response JSON data.
        """
        return await self.request_handler.get_request(*args, **kwargs)

    async def post_request(self, *args, **kwargs):
        """
        Perform an HTTP POST request on the Reddit API.

        Parameters
        ----------
        endpoint: str
            The endpoint to be appended after the base URL (https://oauth.reddit.com/).
        url: str
            The direct URL to perform the request on.
        data:
            The data to add to the POST body.
        kwargs:
            Query parameters to be appended after the URL.

        Returns
        -------
        resp: Dict or None
            The response JSON data.
        """
        return await self.request_handler.post_request(*args, **kwargs)

    async def get_listing(self, endpoint: str, subreddit: Subreddit = None, kind_filter: List[str] = None,
                          **kwargs) -> Listing:
        r"""
        Retrieve a listing from an endpoint.

        Parameters
        ----------
        endpoint: str
            The endpoint to be appended after the base URL (https://oauth.reddit.com/).
        subreddit: Subreddit
            The subreddit to dependency inject into retrieved items when possible.
        kind_filter:
            Kinds to return if given, otherwise all are returned.
        kwargs: \*\*Dict
            Query parameters to be appended after the URL.

        Returns
        -------
        listing: Listing
            The listing containing all the endpoint's children.
        """
        resp = await self.get_request(endpoint, **kwargs)
        return Listing(self, resp["data"], kind_filter=kind_filter, subreddit=subreddit)

    async def subreddit(self, display_name: str) -> Subreddit:
        """
        Get a `Subreddit` object according to the given name.

        Parameters
        ----------
        display_name: str
            The display name of the subreddit.

        Returns
        -------
        subreddit: Subreddit
            The subreddit if found.
        result: None
            Returns None if subreddit not found.
        """
        return await Subreddit(self, {"display_name": display_name}).fetch()

    async def info(self, id: str = "", ids: List[str] = [], url: str = ""):
        """
        Get a Reddit item based on its ID or URL.

        Parameters
        ----------
        id: str
            The item's ID.
        ids: List[str]
            Multiple IDs to fetch multiple items at once (max 100).
        url: str
            The item's URL.

        Yields
        -------
        comment: Comment
            A `Comment` object.
        submission: Submission
            A `Submission` object.
        """
        if id:
            for i in await self.get_listing(API_PATH["info"], id=id):
                yield i
        elif ids:
            while ids:
                for i in await self.get_listing(API_PATH["info"], id=",".join(ids[:100])):
                    yield i
                ids = ids[100:]
        elif url:
            for i in await self.get_listing(API_PATH["info"], url=url):
                yield i
        else:
            yield None

    async def submission(self, id: str = "", url: str = "") -> Submission:
        """
        Get a `Submission` object based on its ID or URL.

        Parameters
        ----------
        id: str
            The ID of a submission (with or without kind).
        url: str
            The URL of a submission.

        Returns
        -------
        submission: Submission
            The requested submission.
        """
        if id != "":
            async for link in self.info(prepend_kind(id, self.link_kind)):
                return link
        elif url != "":
            async for link in self.info(url=url):
                return link
        return None

    async def comment(self, id: str = "", url: str = "") -> Comment:
        """
        Get a `Comment` object based on its ID or URL.

        Parameters
        ----------
        id: str
            The ID of a comment (with or without kind).
        url: str
            The URL of a comment.

        Returns
        -------
        comment: Comment
            The requested comment.
        """
        if id != "":
            comment = Comment(self, {"id": id})
            await comment.fetch()
            return comment
        else:
            comment = Comment(self, {"url": url})
            await comment.fetch()
            return comment

    async def close(self):
        await self.request_handler.close()

    async def redditor(self, username: str) -> Redditor:
        """
        Get a `Redditor` object based the Redditor's username.

        Parameters
        ----------
        username: str
            The Redditor's username (without '/u/').

        Returns
        -------
        redditor: Redditor or None
            The requested Redditor, returns None if not found.
        """
        return await Redditor(self, {"username": username}).fetch()

    async def message(self, to: Union[str, Redditor], subject: str, text: str,
                      from_sr: Union[str, Subreddit] = "") -> Dict:
        """
        Message a Redditor or Subreddit.

        Parameters
        ----------
        to: str or Redditor or Subreddit
            The Redditor or Subreddit the message should be sent to.
        subject: str
            The subject of the message.
        text: str
            The text contents of the message.
        from_sr: str or Subreddit
            Optional if the message is being sent from a subreddit.

        Returns
        -------
        result: Dict
            The response JSON data.
        """
        data = {
            "subject": subject,
            "text": text,
            "to": str(to)
        }
        if from_sr != "":
            data["from_sr"] = str(from_sr)
        resp = await self.post_request(API_PATH["compose"], data=data)
        return resp["success"]


class RequestHandler:

    def __init__(self, user: User):
        self.user = user
        self.queue = []

    async def get_request_headers(self) -> Dict:
        if self.user.token_expires <= datetime.now():
            url = "https://www.reddit.com/api/v1/access_token"
            session = await self.user.auth_session()

            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": self.user.user_agent
            }

            resp = await session.post(url, data=self.user.password_grant, headers=headers)

            async with resp:
                if resp.status == 200:
                    self.user.access_data = await resp.json()
                    self.user.token_expires = datetime.now(
                    ) + timedelta(seconds=self.user.access_data["expires_in"])
                else:
                    raise Exception("Invalid user data.")

        return {
            "Authorization": "{} {}".format(self.user.access_data["token_type"], self.user.access_data["access_token"]),
            "User-Agent": self.user.user_agent
        }

    def update(self, data: CIMultiDictProxy[str]):
        if "x-ratelimit-remaining" in data:
            self.user.ratelimit_remaining = int(float(data["x-ratelimit-remaining"]))
        if "x-ratelimit-used" in data:
            self.user.ratelimit_used = int(data["x-ratelimit-used"])
        if "x-ratelimit-reset" in data:
            self.user.ratelimit_reset = datetime.now() + timedelta(seconds=int(data["x-ratelimit-reset"]))

    async def close(self):
        await self.user.close()

    class Decorators:

        @classmethod
        def check_ratelimit(
                cls, func: Callable[[Any], Awaitable[Any]]) -> Callable[[Any], Awaitable[Any]]:
            @wraps(func)
            async def execute_request(self, *args, **kwargs) -> Any:
                id = datetime.now().strftime('%Y%m%d%H%M%S')
                self.queue.append(id)

                if self.user.ratelimit_remaining < 1:
                    execution_time = self.user.ratelimit_reset + \
                                     timedelta(seconds=len(self.queue))
                    wait_time = (
                            execution_time -
                            datetime.now()).total_seconds()
                    await asyncio.sleep(wait_time)

                result = await func(self, *args, **kwargs)
                self.queue.remove(id)
                return result

            return execute_request

    @Decorators.check_ratelimit
    async def get_request(self, endpoint: str = "", **kwargs) -> Dict:
        kwargs = {"raw_json": 1, "api_type": "json", **kwargs}
        params = ["{}={}".format(k, kwargs[k]) for k in kwargs]

        url = BASE_URL.format(endpoint, "&".join(params))

        headers = await self.get_request_headers()
        session = await self.user.client_session()
        resp = await session.get(url, headers=headers)

        async with resp:
            self.update(resp.headers)
            return await resp.json()

    @Decorators.check_ratelimit
    async def post_request(self, endpoint: str = "", url: str = "", data: Dict = {}, **kwargs) -> Dict:
        kwargs = {"raw_json": 1, "api_type": "json", **kwargs}
        params = ["{}={}".format(k, kwargs[k]) for k in kwargs]

        if endpoint != "":
            url = BASE_URL.format(endpoint, "&".join(params))
        elif url != "":
            url = "{}?{}".format(url, "&".join(params))

        headers = await self.get_request_headers()
        session = await self.user.client_session()
        resp = await session.post(url, data=data, headers=headers)

        async with resp:
            self.update(resp.headers)
            return await resp.json()
