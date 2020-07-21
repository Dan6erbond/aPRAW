from typing import TYPE_CHECKING, Dict, Any

from ..helpers.apraw_base import aPRAWBase
from ..mixins.subreddit import SubredditMixin
from ...const import API_PATH

if TYPE_CHECKING:
    from ...reddit import Reddit
    from .subreddit import Subreddit


class SubredditSettings(aPRAWBase, SubredditMixin):
    """
    A model representing subreddit settings.

    **Typical Attributes**

    This table describes attributes that typically belong to objects of this
    class. Attributes are dynamically provided by the :class:`~apraw.models.aPRAWBase` class
    and may vary depending on the status of the response and expected objects.

    ================================= =============================================================================
    Attribute                         Description
    ================================= =============================================================================
    ``all_original_content``          Whether the subreddit only allows original content.
    ``allow_chat_post_creation``      Whether the subreddit allows chat post creation.
    ``allow_discovery``               Whether this subreddit can be discovered through the recommendations.
    ``allow_galleries``               Whether this subreddit allows submissions with galleries.
    ``allow_images``                  Whether this subreddit allows image posts.
    ``allow_polls``                   Whether this subreddit allows poll posts.
    ``allow_post_crossposts``         Whether this subreddit allows crossposts.
    ``allow_videos``                  Whether this subreddit allows video submissions.
    ``collapse_deleted_comments``     Whether deleted comments in threads should be automatically collapsed.
    ``comment_score_hide_mins``       The comment score below which comments should be hidden.
    ``content_options``               ``string``
    ``crowd_control_chat_level``      ``int``
    ``crowd_control_level``           ``int``
    ``crowd_control_mode``            ``bool``
    ``default_set``                   ``bool``
    ``description``                   The subreddit's short description.
    ``disable_contributor_requests``  ``bool``
    ``domain``                        ``None``
    ``exclude_banned_modqueue``       Whether banned users should be excluded from the modqueue.
    ``free_form_reports``             Whether users can submit custom text reports.
    ``header_hover_text``             The hover text for the subreddit's header.
    ``hide_ads``                      Whether ads should be hidden on this subreddit.
    ``key_color``                     ``string``
    ``language``                      The subreddit's default language as a language code (i.e. "en" for English).
    ``original_content_tag_enabled``  Whether the subreddit has the OC tag enabled.
    ``over_18``                       Whether this subreddit is marked NSFW.
    ``public_description``            The subreddit's public description.
    ``public_traffic``                ``bool``
    ``restrict_commenting``           Whether comments are restricted on the subreddit.
    ``restrict_posting``              Whether posts are restricted on the subreddit.
    ``show_media_preview``            Whether media previews should be displayed by clients.
    ``show_media``                    ``bool``
    ``spam_comments``                 The comment spam filter's setting, either "low", "medium" or "high".
    ``spam_links``                    The link spam filter's setting, either "low", "medium" or "high".
    ``spam_selfposts``                The selfpost spam filter's setting, either "low", "medium" or "high".
    ``spoilers_enabled``              Whether the spoiler marker has been enabled on this subreddit.
    ``submit_link_label``             The submit button's label.
    ``submit_text_label``             The submit text's label.
    ``submit_text``                   ``string``
    ``subreddit_id``                  The ID of the subreddit with the prepended kind i.e. ``t5_``.
    ``subreddit_type``                One of "public", "private" or "restricted".
    ``suggested_comment_sort``        The default comment sort for submissions.
    ``title``                         The subreddit's name.
    ``toxicity_threshold_chat_level`` ``int``
    ``welcome_message_enabled``       Whether the subreddit has enabled welcome messages.
    ``welcome_message_text``          The welcome message's text of this subreddit.
    ``wiki_edit_age``                 The minimum account age requirement for wiki editors.
    ``wiki_edit_karma``               The minimum account karma requirement for wiki editors.
    ``wikimode``                      The mode the wiki is in e.g. "modonly".
    ================================= =============================================================================

   """

    def __init__(self, reddit: 'Reddit', data: Dict[str, Any], subreddit: 'Subreddit' = None):
        """
        Create an instance of ``SubredditSettings``.

        Parameters
        ----------
        reddit: Reddit
            The :class:`~apraw.Reddit` instance with which requests are made.
        data: Dict
            The data obtained from the /about endpoint.
        subreddit: Subreddit
            The subreddit these settings belong to.
        """
        data.update({"subreddit": data.get("subreddit") or data.get("title")})
        aPRAWBase.__init__(self, reddit, data, reddit.subreddit_settings_kind)
        SubredditMixin.__init__(self, subreddit)

    async def fetch(self) -> 'SubredditSettings':
        """
        Fetch this item's information from a suitable API endpoint.

        Returns
        -------
        self: SubredditSettings
            The ``SubredditSettings`` model with updated data.
        """
        sub = self._data.get("subreddit") or self._data.get("title")
        resp = await self._reddit.get(API_PATH["subreddit_settings"].format(sub=sub))
        self._update(resp["data"])
        return self
