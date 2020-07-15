from typing import TYPE_CHECKING, AsyncIterator, Dict, Union, Any

from .moderation import SubredditModerator, SubredditModeration
from .modmail import SubredditModmail
from .wiki import SubredditWiki
from ..helpers.apraw_base import aPRAWBase
from ..helpers.streamable import Streamable, streamable
from ...const import API_PATH

if TYPE_CHECKING:
    from ..reddit.submission import SubmissionKind, Submission
    from ...reddit import Reddit


class Subreddit(aPRAWBase):
    """
    The model representing subreddits.

    Members
    -------
    kind: str
        The item's kind / type.
    mod: SubredditModeration
        Returns an instance of :class:`~apraw.models.SubredditModeration`.
    modmail: SubredditModmail
        Returns an instance of :class:`~apraw.models.SubredditModmail`.
    wiki: SubredditWiki
        Returns an instance of :class:`~apraw.models.SubredditWiki`.

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

    def __init__(self, reddit: 'Reddit', data: Dict = None):
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

        self.mod = SubredditModeration(self)
        self.modmail = SubredditModmail(self)
        self.wiki = SubredditWiki(self)

    async def fetch(self):
        """
        Fetch this item's information from a suitable API endpoint.

        Returns
        -------
        self: Subreddit
            The ``Subreddit`` model with updated data.
        """
        resp = await self._reddit.get_request(API_PATH["subreddit_about"].format(sub=self.display_name))
        self._update(resp["data"])
        return self

    def _update(self, data: Dict[str, Any]):
        """
        Update the base with new information.

        Parameters
        ----------
        data: Dict
            The data obtained from the /about endpoint.
        """
        super()._update(data)
        self.quarantine = data["quarantine"] if "quarantine" in data else False

    async def random(self):
        """
        Retrieve a random submission from the subreddit.

        Returns
        -------
        submission: Submission
            A random submission from the subreddit.
        """
        resp = await self._reddit.get_request(API_PATH["subreddit_random"].format(sub=self))
        from ..reddit.listing import Listing
        listing = Listing(self._reddit, data=resp[0]["data"], subreddit=self)
        return next(listing)

    @streamable
    def comments(self, *args, **kwargs):
        r"""
        Returns an instance of :class:`~apraw.models.ListingGenerator` mapped to the comments endpoint.

        .. note::
            This listing can be streamed doing the following:

            .. code-block:: python3

                for comment in subreddit.comments.stream():
                    print(comment)

        Parameters
        ----------
        kwargs: \*\*Dict
            :class:`~apraw.models.ListingGenerator` ``kwargs``.

        Returns
        -------
        generator: ListingGenerator
            A :class:`~apraw.models.ListingGenerator` mapped to the comments endpoint.
        """
        from ..helpers.generator import ListingGenerator
        return ListingGenerator(self._reddit, API_PATH["subreddit_comments"].format(sub=self.display_name),
                                subreddit=self, *args, **kwargs)

    @streamable
    def new(self, *args, **kwargs):
        r"""
        Returns an instance of :class:`~apraw.models.ListingGenerator` mapped to the new submissions endpoint.

        .. note::
            This listing can be streamed doing the following:

            .. code-block:: python3

                for comment in submissions.new.stream():
                    print(comment)

        Parameters
        ----------
        kwargs: \*\*Dict
            :class:`~apraw.models.ListingGenerator` ``kwargs``.

        Returns
        -------
        generator: ListingGenerator
            A :class:`~apraw.models.ListingGenerator` mapped to the new submissions endpoint.
        """
        from ..helpers.generator import ListingGenerator
        return ListingGenerator(self._reddit, API_PATH["subreddit_new"].format(sub=self.display_name), subreddit=self,
                                *args, **kwargs)

    def hot(self, *args, **kwargs):
        r"""
        Returns an instance of :class:`~apraw.models.ListingGenerator` mapped to the hot submissions endpoint.

        Parameters
        ----------
        kwargs: \*\*Dict
            :class:`~apraw.models.ListingGenerator` ``kwargs``.

        Returns
        -------
        generator: ListingGenerator
            A :class:`~apraw.models.ListingGenerator` mapped to the hot submissions endpoint.
        """
        from ..helpers.generator import ListingGenerator
        return ListingGenerator(self._reddit, API_PATH["subreddit_hot"].format(sub=self.display_name), subreddit=self,
                                *args, **kwargs)

    def rising(self, *args, **kwargs):
        r"""
        Returns an instance of :class:`~apraw.models.ListingGenerator` mapped to the rising submissions endpoint.

        Parameters
        ----------
        kwargs: \*\*Dict
            :class:`~apraw.models.ListingGenerator` ``kwargs``.

        Returns
        -------
        generator: ListingGenerator
            A :class:`~apraw.models.ListingGenerator` mapped to the rising submissions endpoint.
        """
        from ..helpers.generator import ListingGenerator
        return ListingGenerator(self._reddit, API_PATH["subreddit_rising"].format(sub=self.display_name), *args,
                                **kwargs)

    def top(self, *args, **kwargs):
        r"""
        Returns an instance of :class:`~apraw.models.ListingGenerator` mapped to the top submissions endpoint.

        Parameters
        ----------
        kwargs: \*\*Dict
            :class:`~apraw.models.ListingGenerator` ``kwargs``.

        Returns
        -------
        generator: ListingGenerator
            A :class:`~apraw.models.ListingGenerator` mapped to the top submissions endpoint.
        """
        from ..helpers.generator import ListingGenerator
        return ListingGenerator(self._reddit, API_PATH["subreddit_top"].format(sub=self.display_name), subreddit=self,
                                *args, **kwargs)

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
        r"""
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
        req = await self._reddit.get_request(API_PATH["subreddit_moderators"].format(sub=self.display_name), **kwargs)
        for u in req["data"]["children"]:
            yield SubredditModerator(self._reddit, u)

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
        return await self._reddit.message(API_PATH["subreddit"].format(sub=self.display_name), subject, text,
                                          str(from_sr))

    async def submit(self, title: str, kind: 'SubmissionKind', **kwargs) -> 'Submission':
        """
        Make a new post to the subreddit.
        If `kind` is SubmissionKind.LINK then `url` is expected to be a valid url,
        otherwise `text` is expected (and it can be markdown text)

        Parameters
        -------
        title: str
            The post's title.
        kind: SubmissionKind
            The post's kind.
        url: str
            Optional, the url if kind is LINK.
        text: str
            Optional, the text body of the post.
        nsfw: bool = False
            If the post if nsfw or not.
        resubmit: bool = False
            If the post is a re-submit or not.
            Needs to be True if a link with the same URL has already been submitted to the specified subreddi
        spoiler: bool = False
            If the post is a spoiler or not.
        """
        from ..reddit.submission import Submission, SubmissionKind

        url = kwargs.get("url", None)
        text = kwargs.get("text", None)

        if kind == SubmissionKind.LINK and not url:
            raise ValueError("A url was expected")
        if kind == SubmissionKind.SELF and not text:
            raise ValueError("A text body was expected")

        resp = await self._reddit.post_request(API_PATH["submit"], **{
            "sr": str(self),
            "title": title,
            "kind": kind.value,
            "url": url,
            "text": text,
            "nsfw": kwargs.get("nsfw", False),
            "resubmit": kwargs.get("resubmit", False),
            "spoiler": kwargs.get("spoiler", False)
        })

        submission = Submission(self._reddit, {"id": resp["json"]["data"]["id"]})
        await submission.fetch()

        return submission
