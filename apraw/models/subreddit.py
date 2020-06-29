from datetime import datetime
from typing import TYPE_CHECKING, AsyncIterator, Dict, Union

from ..endpoints import API_PATH
from ..utils import snake_case_keys
from .helpers.apraw_base import aPRAWBase
from .modmail import SubredditModmail
from .redditor import Redditor
from .subreddit_wiki import SubredditWiki

if TYPE_CHECKING:
    from ..reddit import Reddit


class Subreddit(aPRAWBase):
    """
    The model representing subreddits.

    Members
    -------
    reddit: Reddit
        The :class:`~apraw.Reddit` instance with which requests are made.
    data: Dict
        The data obtained from the /about endpoint.
    kind: str
        The item's kind / type.
    mod: SubredditModeration
        Returns an instance of :class:`~apraw.models.SubredditModeration`.
    modmail: SubredditModmail
        Returns an instance of :class:`~apraw.models.SubredditModmail`.
    wiki: SubredditWiki
        Returns an instance of :class:`~apraw.models.SubredditWiki`.
    comments: ListingGenerator
        Returns an instance of :class:`~apraw.models.ListingGenerator` mapped to the comments endpoint.
    new: ListingGenerator
        Returns an instance of :class:`~apraw.models.ListingGenerator` mapped to the new submissions endpoint.
    hot: ListingGenerator
        Returns an instance of :class:`~apraw.models.ListingGenerator` mapped to the hot submissions endpoint.
    rising: ListingGenerator
        Returns an instance of :class:`~apraw.models.ListingGenerator` mapped to the rising submissions endpoint.
    top: ListingGenerator
        Returns an instance of :class:`~apraw.models.ListingGenerator` mapped to the top submissions endpoint.

    .. warning::
        Using the streams of non-new endpoints may result in receiving items multiple times, as their positions can change and be returned by the API after they've been removed from the internal tracker.

    **Examples**

    To grab new submissions made on a subreddit:

    .. code-block:: python3

        sub = await reddit.subreddit("aprawtest")
        async for submission in sub.new(): # use .new.stream() for endless polling
            print(submission.title, submission.body)

    **Typical Attributes**

    This table describes attributes that typically belong to objects of this
    class. Attributes are dynamically provided by the :class:`~apraw.models.aPRAWBase` class
    and may vary depending on the status of the response and expected objects.

    ================================ ==================================================================
    Attribute                        Description
    ================================ ==================================================================
    ``accounts_active_is_fuzzed``    ``bool``
    ``accounts_active``              ``null``
    ``active_user_count``            The number of active users on the subreddit.
    ``advertiser_category``          ``string``
    ``all_original_content``         Whether the subreddit requires all content to be OC.
    ``allow_discovery``              Whether the subreddit can be discovered.
    ``allow_images``                 Whether images are allowed as submissions.
    ``allow_videogifs``              Whether GIFs are allowed as submissions.
    ``allow_videos``                 Whether videos are allowed as submissions.
    ``banner_background_color``      The banner's background color if applicable, otherwise empty.
    ``banner_background_image``      A URL to the subreddit's banner image.
    ``banner_img``                   A URL to the subreddit's banner image if applicable.
    ``banner_size``                  The subreddit's banner size if applicable.
    ``can_assign_link_flair``        Whether submission flairs can be assigned.
    ``can_assign_user_flair``        Whether the user can assign their own flair on the subreddit.
    ``collapse_deleted_comments``    Whether deleted comments should be deleted by clients.
    ``comment_score_hide_mins``      The minimum comment score to hide.
    ``community_icon``               A URL to the subreddit's community icon if applicable.
    ``created_utc``                  The date on which the subreddit was created in UTC ``datetime``.
    ``created``                      The time the subreddit was created on.
    ``description_html``             The subreddit's description as HTML.
    ``description``                  The subreddit's short description.
    ``disable_contributor_requests`` ``bool``
    ``display_name_prefixed``        The subreddit's display name prefixed with 'r/'.
    ``display_name``                 The subreddit's display name.
    ``emojis_custom_size``           The custom size set for emojis.
    ``emojis_enabled``               Whether emojis are enabled on this subreddit.
    ``free_form_reports``            Whether it's possible to submit free form reports.
    ``has_menu_widget``              Whether the subreddit has menu widgets.
    ``header_img``                   A URL to the subreddit's header image of applicable.
    ``header_size``                  The subreddit's header size.
    ``header_title``                 The subreddit's header title.
    ``hide_ads``                     Whether ads are hidden on this subreddit.
    ``icon_img``                     A URL to the subreddit's icon image of applicable.
    ``icon_size``                    The subreddit's icon size.
    ``id``                           The subreddit's ID.
    ``is_enroled_in_new_modmail``    Whether the subreddit is enrolled in new modmail.
    ``key_color``                    ``string``
    ``lang``                         The subreddit's language.
    ``link_flair_enabled``           Whether link flairs have been enabled for the subreddit.
    ``link_flair_position``          The position of link flairs.
    ``mobile_banner_size``           A URL to the subreddit's mobile banner if applicable.
    ``name``                         The subreddit's fullname (t5_ID).
    ``notification_level``
    ``original_content_tag_enabled`` Whether the subreddit has the OC tag enabled.
    ``over18``                       Whether the subreddit is NSFW.
    ``primary_color``                The subreddit's primary color.
    ``public_description_html``      The subreddit's public description as HTML.
    ``public_description``           The subreddit's public description string.
    ``public_traffic``               ``bool``
    ``quarantine``                   Whether the subreddit is quarantined.
    ``restrict_commenting``             Whether comments by users are restricted on the subreddit.
    ``restrict_posting``             Whether posts to the subreddit are restricted.
    ``show_media_preview``           Whether media previews should be displayed by clients.
    ``show_media``
    ``spoilers_enabled``             Whether the spoiler tag is enabled on the subreddit.
    ``submission_type``              The types of allowed submissions. Default is "any".
    ``submit_link_label``            The subreddit's submit label if applicable.
    ``submit_text_html``             The HTML submit text if a custom one is set on the subreddit.
    ``submit_text_label``            The text used for the submit button.
    ``submit_text``                  The markdown submit text if a custom one is set on the subreddit.
    ``subreddit_type``               The subreddit type, either "public", "restricted" or "private".
    ``subscribers``                  The number of subreddit subscribers.
    ``suggested_comment_sort``       The suggested comment sort algorithm, can be ``null``.
    ``title``                        The subreddit's banner title.
    ``url``                          The subreddit's display name prepended with "/r/".
    ``user_can_flair_in_sr``         Whether the user can assign custom flairs (nullable).
    ``user_flair_background_color``  The logged in user's flair background color if applicable.
    ``user_flair_css_class``         The logged in user's flair CSS class.
    ``user_flair_enabled_in_sr``     Whether the logged in user's subreddit flair is enabled.
    ``user_flair_position``          The position of user flairs on the subreddit (right or left).
    ``user_flair_richtext``          The logged in user's flair text if applicable.
    ``user_flair_template_id``       The logged in user's flair template ID if applicable.
    ``user_flair_text_color``        The logged in user's flair text color.
    ``user_flair_text``              The logged in user's flair text.
    ``user_flair_type``              The logged in user's flair type.
    ``user_has_favorited``           Whether the logged in user has favorited the subreddit.
    ``user_is_banned``               Whether the logged in user is banned from the subreddit.
    ``user_is_contributor``          Whether the logged in user has contributed to the subreddit.
    ``user_is_moderator``            Whether the logged in user is a moderator on the subreddit.
    ``user_is_muted``                Whether the logged in user has been muted by the subreddit.
    ``user_is_subscriber``           Whether the logged in user is subscribed to the subreddit.
    ``user_sr_flair_enabled``        Whether the logged in user's subreddit flair is enabled.
    ``user_sr_theme_enabled``        Whether the logged in user has enabled the custom subreddit theme.
    ``videostream_links_count``      The number of submissions with videostream links.
    ``whitelist_status``
    ``wiki_enabled``                 Whether the subreddit has the wiki enabled.
    ``wls``                          ``null``
    ================================ ==================================================================
    """

    def __init__(self, reddit: 'Reddit', data: Dict):
        """
        Create a Subreddit instance.

        Parameters
        ----------
        reddit: Reddit
            The :class:`~apraw.Reddit` instance with which requests are made.
        data: Dict
            The data obtained from the /about endpoint.
        """
        super().__init__(reddit, data, reddit.subreddit_kind)

        self.quarantine = data["quarantine"] if "quarantine" in data else False

        self.mod = SubredditModeration(self)
        self.modmail = SubredditModmail(self)
        self.wiki = SubredditWiki(self)

        from .helpers.listing_generator import ListingGenerator
        self.comments = ListingGenerator(
            self.reddit, API_PATH["subreddit_comments"].format(
                sub=self.display_name), subreddit=self)
        self.new = ListingGenerator(self.reddit,
                                    API_PATH["subreddit_new"].format(sub=self.display_name), subreddit=self)
        self.hot = ListingGenerator(self.reddit,
                                    API_PATH["subreddit_hot"].format(sub=self.display_name), subreddit=self)
        self.rising = ListingGenerator(
            self.reddit, API_PATH["subreddit_rising"].format(sub=self.display_name))
        self.top = ListingGenerator(self.reddit,
                                    API_PATH["subreddit_top"].format(sub=self.display_name), subreddit=self)

    def __str__(self):
        """
        Returns the subreddit's name as a string.

        Returns
        -------
        display_name: str
            The subreddit's name as a string.
        """
        return self.display_name

    async def moderators(self, **kwargs) -> AsyncIterator['SubredditModerator']:
        """
        Yields all the subreddit's moderators.

        Parameters
        ----------
        kwargs: \*\*Dict
            The query parameters to be added to the GET request.

        Yields
        ------
        moderator: SubredditModerator
            An instance of the moderators as :class:`~apraw.models.SubredditModerator`.
        """
        req = await self.reddit.get_request(API_PATH["subreddit_moderators"].format(sub=self.display_name), **kwargs)
        for u in req["data"]["children"]:
            yield SubredditModerator(self.reddit, u)

    async def message(self, subject: str, text: str, from_sr: Union[str, 'Subreddit'] = "") -> Dict:
        """
        Send a message to the subreddit.

        Parameters
        ----------
        subject: str
            The message subject.
        text: str
            The message contents as markdown.
        from_sr: str or Subreddit
            The subreddit the message is being sent from if applicable.
        Returns
        -------
        response: Dict
            The API response JSON as a dictionary.
        """
        return await self.reddit.message(API_PATH["subreddit"].format(sub=self.display_name), subject, text, str(from_sr))


class SubredditModerator(aPRAWBase):
    """
    The model representing subreddit moderators. Redditors can be retrieved via ``redditor()``.

    **Typical Attributes**

    This table describes attributes that typically belong to objects of this
    class. Attributes are dynamically provided by the :class:`~apraw.models.aPRAWBase` class
    and may vary depending on the status of the response and expected objects.

    ========================== ============================================================
    Attribute                  Description
    ========================== ============================================================
    ``added``                  The date on which the moderator was added.
    ``author_flair_css_class`` The moderator's flair CSS class in the respective subreddit.
    ``author_flair_text``      The moderator's flair text in the respective subreddit.
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
        super().__init__(reddit, data)

        self.added = datetime.utcfromtimestamp(data["date"])

    def __str__(self):
        """
        Returns the Redditor's name.

        Returns
        -------
        name: str
            The Redditor's name.
        """
        return self.name

    async def redditor(self) -> Redditor:
        """
        Retrieve the Redditor this Moderator represents.

        Returns
        -------
        redditor: Redditor
            The Redditor that is represented by this object.
        """
        return await self.reddit.redditor(self.name)


class SubredditModeration:
    """
    A helper class for grabbing listings to Subreddit moderation items.

    Members
    -------
    reports: ListingGenerator
        Returns an instance of :class:`~apraw.models.ListingGenerator` mapped to grab reported items.
    spam: ListingGenerator
        Returns an instance of :class:`~apraw.models.ListingGenerator` mapped to grab items marked as spam.
    modqueue: ListingGenerator
        Returns an instance of :class:`~apraw.models.ListingGenerator` mapped to grab items in the modqueue.
    unmoderated: ListingGenerator
        Returns an instance of :class:`~apraw.models.ListingGenerator` mapped to grab unmoderated items.
    edited: ListingGenerator
        Returns an instance of :class:`~apraw.models.ListingGenerator` mapped to grab edited items.
    log: ListingGenerator
        Returns an instance of :class:`~apraw.models.ListingGenerator` mapped to grab mod actions in the subreddit log.
    """

    def __init__(self, subreddit):
        self.subreddit = subreddit

        from .helpers.listing_generator import ListingGenerator
        self.reports = ListingGenerator(
            self.subreddit.reddit,
            API_PATH["subreddit_reports"].format(
                sub=self.subreddit.display_name), subreddit=self.subreddit)
        self.spam = ListingGenerator(
            self.subreddit.reddit,
            API_PATH["subreddit_spam"].format(
                sub=self.subreddit.display_name), subreddit=self.subreddit)
        self.modqueue = ListingGenerator(
            self.subreddit.reddit,
            API_PATH["subreddit_modqueue"].format(
                sub=self.subreddit.display_name), subreddit=self.subreddit)
        self.unmoderated = ListingGenerator(
            self.subreddit.reddit,
            API_PATH["subreddit_unmoderated"].format(
                sub=self.subreddit.display_name), subreddit=self.subreddit)
        self.edited = ListingGenerator(
            self.subreddit.reddit,
            API_PATH["subreddit_edited"].format(
                sub=self.subreddit.display_name), subreddit=self.subreddit)
        self.log = ListingGenerator(
            self.subreddit.reddit,
            API_PATH["subreddit_log"].format(
                sub=self.subreddit.display_name), subreddit=self.subreddit)


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
        return await self.subreddit.reddit.redditor(self.mod)
