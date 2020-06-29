from typing import TYPE_CHECKING, Dict

from ..endpoints import API_PATH
from .helpers.apraw_base import aPRAWBase

if TYPE_CHECKING:
    from .subreddit import Subreddit
    from ..reddit import Reddit


class Redditor(aPRAWBase):
    """
    The model representing Redditors.

    Members
    -------
    reddit: Reddit
        The :class:`~apraw.Reddit` instance with which requests are made.
    data: Dict
        The data obtained from the /about endpoint.
    kind: str
        The item's kind / type.
    comments: ListingGenerator
        Returns an instance of :class:`~apraw.models.ListingGenerator` mapped to fetch the Redditor's comments.
    submissions: ListingGenerator
        Returns an instance of :class:`~apraw.models.ListingGenerator` mapped to fetch the Redditor's submission.
    subreddit: Sureddit
        An instance of :class:`~apraw.models.Subreddit` for the Redditor's profile subreddit.

    **Typical Attributes**

    This table describes attributes that typically belong to objects of this
    class. Attributes are dynamically provided by the :class:`~apraw.models.aPRAWBase` class
    and may vary depending on the status of the response and expected objects.

    ======================== ================================================================
    Attribute                Description
    ======================== ================================================================
    ``comment_karma``        The amount of comment karma the Redditor has obtained.
    ``created_utc``          The date on which the Redditor was created in UTC ``datetime``.
    ``created``              The timestamp of when the Redditor was created.
    ``has_verified_email``   Whether the Redditor has a verified email address.
    ``icon_img``             A URL to the Redditor's icon image if applicable.
    ``id``                   The Redditor's ID (without kind).
    ``is_employee``          Whether the Redditor is a Reddit employee.
    ``is_friend``            Whether the Redditor has been added as a friend.
    ``is_gold``              Whether the Redditor is a Reddit gold member.
    ``is_mod``               Whether the Redditor is a moderator in a subreddit.
    ``is_suspended``         Whether the Redditor has been suspended.
    ``link_karma``           The amount of link karma the Redditor has obtained.
    ``name``                 The Redditor's username.
    ``pref_show_snoovatar``  Whether to show the Redditor's Snoovatar in place of their icon.
    ``verified``             Whether the Redditor is verified.
    ======================== ================================================================

    .. warning::
        Suspended Redditors only return ``is_suspended`` and ``name``.

    """

    def __init__(self, reddit: 'Reddit', data: Dict):
        """
        Create a Redditor instance.

        Parameters
        ----------
        reddit: Reddit
            The :class:`~apraw.Reddit` instance with which requests are made.
        data: Dict
            The data obtained from the /about endpoint.
        """
        super().__init__(reddit, data, reddit.account_kind)

        self.reddit = reddit
        self.data = data

        self.is_suspended = "is_suspended" not in data or not data["is_suspended"]

        if "subreddit" in data and data["subreddit"]:
            sub = data["subreddit"]
            sub["id"] = sub["name"].replace("t5_", "")
            if "created_utc" not in sub:
                sub["created_utc"] = data["created_utc"]
            from .subreddit import Subreddit
            self.subreddit = Subreddit(self.reddit, sub)
        else:
            self.subreddit = None

        from .helpers.listing_generator import ListingGenerator
        self.comments = ListingGenerator(
            self.reddit,
            API_PATH["user_comments"].format(
                user=self))
        self.submissions = ListingGenerator(
            self.reddit,
            API_PATH["user_submissions"].format(
                user=self))

    def __str__(self):
        """
        Returns the Redditor's name.

        Returns
        -------
        name:   str
            The Redditor's username.
        """
        return self.name

    async def moderated_subreddits(self, **kwargs) -> 'Subreddit':
        """
        Yields the subreddits the Redditor moderates.

        Parameters
        ----------
        kwargs: \*\*Dict
            ``kwargs`` to be used as query parameters.

        Yields
        ------
        subreddit: Subreddit
            A subreddit the user moderates.
        """
        req = await self.reddit.get_request(API_PATH["moderated"].format(user=self), **kwargs)
        for s in req["data"]:
            yield await self.reddit.subreddit(s["sr"])

    async def message(self, subject, text, from_sr="") -> Dict:
        """
        Message the Redditor.

        Parameters
        ----------
        subject: str
            The subject of the message.
        text: str
            The text contents of the message in markdown.
        from_sr: str
            The subreddit the message is being sent from if applicable.

        Returns
        -------
        resp: Dict
            The response data returned from the endpoint.
        """
        return await self.reddit.message(self.name, subject, text, from_sr)
