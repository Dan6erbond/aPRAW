from datetime import datetime
from typing import Dict, TYPE_CHECKING

from .settings import SubredditSettings
from ..helpers.apraw_base import aPRAWBase
from ..helpers.streamable import streamable
from ..mixins.redditor import RedditorMixin
from ..reddit.redditor import Redditor
from ...const import API_PATH

if TYPE_CHECKING:
    from ...reddit import Reddit
    from .subreddit import Subreddit


class SubredditModerator(aPRAWBase, RedditorMixin):
    """
    The model representing subreddit moderators. Redditors can be retrieved via
    :meth:`~apraw.models.SubredditModerator.redditor()`.

    **Typical Attributes**

    This table describes attributes that typically belong to objects of this
    class. Attributes are dynamically provided by the :class:`~apraw.models.aPRAWBase` class
    and may vary depending on the status of the response and expected objects.

    ========================== ============================================================
    Attribute                  Description
    ========================== ============================================================
    ``added``                  The parsed UTC date on which the moderator was added.
    ``author_flair_css_class`` The moderator's flair CSS class in the respective subreddit.
    ``author_flair_text``      The moderator's flair text in the respective subreddit.
    ``date``                   The UTC timestamp on which the moderator was added.
    ``id``                     The Redditor's fullname (t2_ID).
    ``mod_permissions``        A list of all the moderator permissions or ``["all"]``.
    ``name``                   The Redditor's name.
    ========================== ============================================================

    """

    def __init__(self, reddit: 'Reddit', data: Dict):
        """
        Create a SubredditModerator instance.

        Parameters
        ----------
        reddit: Reddit
            The :class:`~apraw.Reddit` instance with which requests are made.
        data: Dict
            The data obtained from the API.
        """
        if "date" in data:
            data["added"] = datetime.utcfromtimestamp(data["date"])
        super().__init__(reddit, data, reddit.account_kind)


class SubredditModeration:
    """
    A helper class for grabbing listings to Subreddit moderation items.

    """

    def __init__(self, reddit: 'Reddit', subreddit: 'Subreddit'):
        """
        Create an instance of ``SubredditModeration``.

        Parameters
        ----------
        reddit: Reddit
            The :class:`~apraw.Reddit` instance with which requests are made.
        subreddit: Subreddit
            The subreddit this helper instance belongs to and performs requests for.
        """
        self._reddit = reddit
        self._subreddit = subreddit
        self._settings = None

    #: Streamable listing endpoint.
    @streamable
    def reports(self, *args, **kwargs):
        r"""
        Returns an instance of :class:`~apraw.models.ListingGenerator` mapped to grab reported items.

        .. note::
            This listing can be streamed doing the following:

            .. code-block:: python3

                for comment in subreddit.mod.reports.stream():
                    print(comment)

        Parameters
        ----------
        kwargs: \*\*Dict
            :class:`~apraw.models.ListingGenerator` ``kwargs``.

        Returns
        -------
        generator: ListingGenerator
            A :class:`~apraw.models.ListingGenerator` mapped to grab reported items.
        """
        from ..helpers.generator import ListingGenerator
        return ListingGenerator(self._reddit,
                                API_PATH["subreddit_reports"].format(sub=self._subreddit.display_name),
                                subreddit=self._subreddit, *args, **kwargs)

    #: Streamable listing endpoint.
    @streamable
    def spam(self, *args, **kwargs):
        r"""
        Returns an instance of :class:`~apraw.models.ListingGenerator` mapped to grab items marked as spam.

        .. note::
            This listing can be streamed doing the following:

            .. code-block:: python3

                for comment in subreddit.mod.spam.stream():
                    print(comment)

        Parameters
        ----------
        kwargs: \*\*Dict
            :class:`~apraw.models.ListingGenerator` ``kwargs``.

        Returns
        -------
        generator: ListingGenerator
            A :class:`~apraw.models.ListingGenerator` mapped to grab items marked as spam.
        """
        from ..helpers.generator import ListingGenerator
        return ListingGenerator(self._reddit,
                                API_PATH["subreddit_spam"].format(sub=self._subreddit.display_name),
                                subreddit=self._subreddit, *args, **kwargs)

    #: Streamable listing endpoint.
    @streamable
    def modqueue(self, *args, **kwargs):
        r"""
        Returns an instance of :class:`~apraw.models.ListingGenerator` mapped to grab items in the modqueue.

        .. note::
            This listing can be streamed doing the following:

            .. code-block:: python3

                for comment in subreddit.mod.modqueue.stream():
                    print(comment)

        Parameters
        ----------
        kwargs: \*\*Dict
            :class:`~apraw.models.ListingGenerator` ``kwargs``.

        Returns
        -------
        generator: ListingGenerator
            A :class:`~apraw.models.ListingGenerator` mapped to grab items in the modqueue.
        """
        from ..helpers.generator import ListingGenerator
        return ListingGenerator(self._reddit,
                                API_PATH["subreddit_modqueue"].format(sub=self._subreddit.display_name),
                                subreddit=self._subreddit, *args, **kwargs)

    #: Streamable listing endpoint.
    @streamable
    def unmoderated(self, *args, **kwargs):
        r"""
        Returns an instance of :class:`~apraw.models.ListingGenerator` mapped to grab unmoderated items.

        .. note::
            This listing can be streamed doing the following:

            .. code-block:: python3

                for comment in subreddit.mod.unmoderated.stream():
                    print(comment)

        Parameters
        ----------
        kwargs: \*\*Dict
            :class:`~apraw.models.ListingGenerator` ``kwargs``.

        Returns
        -------
        generator: ListingGenerator
            A :class:`~apraw.models.ListingGenerator` mapped to grab unmoderated items.
        """
        from ..helpers.generator import ListingGenerator
        return ListingGenerator(self._reddit,
                                API_PATH["subreddit_unmoderated"].format(sub=self._subreddit.display_name),
                                subreddit=self._subreddit, *args, **kwargs)

    #: Streamable listing endpoint.
    @streamable
    def edited(self, *args, **kwargs):
        r"""
        Returns an instance of :class:`~apraw.models.ListingGenerator` mapped to grab edited items.

        .. note::
            This listing can be streamed doing the following:

            .. code-block:: python3

                for comment in subreddit.mod.edited.stream():
                    print(comment)

        Parameters
        ----------
        kwargs: \*\*Dict
            :class:`~apraw.models.ListingGenerator` ``kwargs``.

        Returns
        -------
        generator: ListingGenerator
            A :class:`~apraw.models.ListingGenerator` mapped to grab edited items.
        """
        from ..helpers.generator import ListingGenerator
        return ListingGenerator(self._reddit,
                                API_PATH["subreddit_edited"].format(sub=self._subreddit.display_name),
                                subreddit=self._subreddit, *args, **kwargs)

    #: Streamable listing endpoint.
    @streamable
    def log(self, *args, **kwargs):
        r"""
        Returns an instance of :class:`~apraw.models.ListingGenerator` mapped to grab mod actions in the subreddit log.

        .. note::
            This listing can be streamed doing the following:

            .. code-block:: python3

                for comment in subreddit.mod.log.stream():
                    print(comment)

        Parameters
        ----------
        kwargs: \*\*Dict
            :class:`~apraw.models.ListingGenerator` ``kwargs``.

        Returns
        -------
        generator: ListingGenerator
            A :class:`~apraw.models.ListingGenerator` mapped to grab mod actions in the subreddit log.
        """
        from ..helpers.generator import ListingGenerator
        return ListingGenerator(self._reddit,
                                API_PATH["subreddit_log"].format(sub=self._subreddit.display_name),
                                subreddit=self._subreddit, *args, **kwargs)

    async def settings(self) -> SubredditSettings:
        """
        Retrieve the settings for the subreddit this helper works for.

        Returns
        -------
        settings: SubredditSettings
            The subreddit's settings with their data prefetched.
        """
        if not self._settings:
            self._settings = SubredditSettings(self._reddit,
                                               {"subreddit": self._subreddit.display_name},
                                               self._subreddit)
            await self._settings.fetch()
        return self._settings


class ModAction(aPRAWBase):
    """
    A model representing mod actions taken on specific items.

    Members
    -------
    reddit: Reddit
        The :class:`~apraw.Reddit` instance with which requests are made.
    data: Dict
        The data obtained from the /about endpoint.
    kind: str
        The item's kind / type.

    **Typical Attributes**

    This table describes attributes that typically belong to objects of this
    class. Attributes are dynamically provided by the :class:`~apraw.models.aPRAWBase` class
    and may vary depending on the status of the response and expected objects.

    =========================== =========================================================================
    Attribute                   Description
    =========================== =========================================================================
    ``action``                  The type of action performed.
    ``created_utc``             The parsed UTC datetime of when the action was performed.
    ``description``             The description added to the action if applicable.
    ``details``                 The details of the action performed.
    ``id``                      The ID of the mod action prepended with "ModAction_".
    ``mod_id36``                The ID36 of the moderator who performed the action.
    ``mod``                     The username of the moderator who performed the action.
    ``sr_id36``                 The ID36 of the subreddit the action was performed on.
    ``subreddit_name_prefixed`` The name of the subreddit the action was performed on prefixed with "r/".
    ``subreddit``               The name of the subreddit the action was performed on.
    ``target_author``           The author of the target item if applicable.
    ``target_body``             The body of the target item if applicable.
    ``target_fullname``         The id of the target with its kind prepended. (e.g. "t3_d5229o")
    ``target_permalink``        The target of the comment or submission if applicable.
    ``target_title``            The title of the submission if applicable.
    =========================== =========================================================================
    """

    def __init__(self, reddit, data, subreddit=None):
        """
        Create an instance of a ModAction.

        Parameters
        ----------
        data: Dict
            The data returned from the API endpoint.
        subreddit: Subreddit
            The subreddit this ModAction belongs to.
        """
        super().__init__(reddit, data, reddit.modaction_kind)

        self.subreddit = subreddit

    async def mod(self) -> Redditor:
        """
        Returns the Redditor who performed this action.

        Returns
        -------
        redditor: Redditor
            The Redditor who performed this action.
        """
        return await self.subreddit._reddit.redditor(self._data["mod"])
