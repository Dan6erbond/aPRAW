import asyncio
import configparser
import os
from typing import Dict, List, Union, Any

from .endpoints import API_PATH
from .models import (Comment, Listing, Redditor, Submission,
                     Subreddit, User, ListingGenerator, streamable)
from .request_handler import RequestHandler
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
    comment_kind: str
        The prefix that represents :class:`~apraw.models.Comment` in API responses, such as ``t1``.
    account_kind: str
        The prefix that represents :class:`~apraw.models.Redditor` in API responses, such as ``t2``.
    link_kind: str
        The prefix that represents :class:`~apraw.models.Submission` in API responses, such as ``t3``.
    message_kind: str
        The prefix that represents :class:`~apraw.models.Message` in API responses, such as ``t4``.
    subreddit_kind: str
        The prefix that represents :class:`~apraw.models.Subreddit` in API responses, such as ``t5``.
    award_kind: str
        The prefix that represents awards in API responses, such as ``t6``.
    modaction_kind: str
        The prefix that represents :class:`~apraw.models.ModAction` in API responses, such as ``modaction``.
    listing_kind: str
        The prefix that represents :class:`~apraw.models.Listing` in API responses, such as ``listing``.
    wiki_revision_kind: str
        The prefix that represents :class:`~apraw.models.WikipageRevision` in API responses, such as ``WikiRevision``.
    wikipage_kind: str
        The prefix that represents :class:`~apraw.models.SubredditWikipage` in API responses, such as ``wikipage``.
    more_kind: str
        The prefix that represents :class:`~apraw.models.MoreComments` in API responses, such as ``more``.
    request_handler: RequestHandler
        An instance of :class:`~apraw.RequestHandler` with which this Reddit instance will perform HTTP requests.
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
        self.subreddit_settings_kind = "subreddit_settings"

        self.loop = asyncio.get_event_loop()
        self.request_handler = RequestHandler(self.user)

    #: Streamable listing endpoint.
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

    async def get(self, *args, **kwargs) -> Any:
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
        resp: Any
            The response JSON data.
        """
        return await self.request_handler.get(*args, **kwargs)

    async def post(self, *args, **kwargs) -> Any:
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
        resp: Any
            The response JSON data.
        """
        return await self.request_handler.post(*args, **kwargs)

    async def put(self, *args, **kwargs) -> Any:
        """
        Perform an HTTP PUT request on the Reddit API.

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
        resp: Any
            The response JSON data.
        """
        return await self.request_handler.put(*args, **kwargs)

    async def delete(self, *args, **kwargs) -> Any:
        """
        Perform an HTTP DELETE request on the Reddit API.

        Parameters
        ----------
        endpoint: str
            The endpoint to be appended after the base URL (https://oauth.reddit.com/).
        url: str
            The direct URL to perform the request on.
        kwargs:
            Query parameters to be appended after the URL.

        Returns
        -------
        resp: Any
            The response JSON data.
        """
        return await self.request_handler.post(*args, **kwargs)

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
        resp = await self.get(endpoint, **kwargs)
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
        """
        sub = Subreddit(self, {"display_name": display_name})
        await sub.fetch()
        return sub

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
            submission = Submission(self, {"id": id})
            await submission.fetch()
            return submission
        else:
            submission = Submission(self, {"url": url})
            await submission.fetch()
            return submission

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
                      from_sr: Union[str, Subreddit] = "") -> bool:
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
        resp = await self.post(API_PATH["compose"], data=data)
        return not resp["json"]["errors"]
