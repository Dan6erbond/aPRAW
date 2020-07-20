from enum import Enum
from typing import TYPE_CHECKING, Dict, List, Any, Union

from .redditor import Redditor
from ..helpers.apraw_base import aPRAWBase
from ..helpers.item_moderation import PostModeration
from ..mixins.author import AuthorMixin
from ..mixins.deletable import DeletableMixin
from ..mixins.hideable import HideableMixin
from ..mixins.nsfwable import NSFWableMixin
from ..mixins.replyable import ReplyableMixin
from ..mixins.savable import SavableMixin
from ..mixins.spoilerable import SpoilerableMixin
from ..mixins.subreddit import SubredditMixin
from ..mixins.votable import VotableMixin
from ..subreddit.subreddit import Subreddit
from ...const import API_PATH
from ...utils import prepend_kind

if TYPE_CHECKING:
    from ...reddit import Reddit


class SubmissionKind(Enum):
    """
    An enum representing the valid submission kinds
    """
    LINK = "link"
    SELF = "self"
    IMAGE = "image"
    VIDEO = "video"
    VIDEOGIF = "videogif"


class Submission(aPRAWBase, DeletableMixin, HideableMixin, ReplyableMixin, NSFWableMixin, SavableMixin, VotableMixin,
                 AuthorMixin, SubredditMixin, SpoilerableMixin):
    """
    The model representing submissions.

    Members
    -------
    reddit: Reddit
        The :class:`~apraw.Reddit` instance with which requests are made.
    data: Dict
        The data obtained from the /about endpoint.
    mod: SubmissionModeration
        The :class:`~apraw.models.SubmissionModeration` instance to aid in moderating the submission.
    kind: str
        The item's kind / type.

    **Typical Attributes**

    This table describes attributes that typically belong to objects of this
    class. Attributes are dynamically provided by the :class:`~apraw.models.aPRAWBase` class
    and may vary depending on the status of the response and expected objects.

    ================================= ============================================================================
    Attribute                         Description
    ================================= ============================================================================
    ``all_awardings``                 A list of the awardings on the submission.
    ``allow_live_comments``           Whether live comments have been enabled on this submission.
    ``approved_at_utc``               The UTC timestamp of when the submission was approved.
    ``approved_by``                   The user that approved the submission.
    ``approved``                      Whether the submission has been approved by the moderators of the subreddit.
    ``archived``                      Whether the submission has been archived by Reddit.
    ``author_flair_background_color`` The submission author's flair background color.
    ``author_flair_css_class``        The submission's author flair CSS class.
    ``author_flair_richtext``         The submission's author flair text.
    ``author_flair_template_id``      The submission author's flair template ID if applicable.
    ``author_flair_text_color``       The submission's author flair text color if applicable.
    ``author_flair_text``             The author's flair text if applicable.
    ``author_flair_type``             The type of flair used by the submission's author.
    ``author_fullname``               The author of the submission prepended with ``t2_``.
    ``author_patreon_flair``          The submission's author Patreon flair.
    ``author``                        The name of the submission's Redditor.
    ``banned_at_utc``                 The UTC timestamp at which the author was banned.
    ``banned_by``                     ``null``
    ``can_gild``                      Whether the logged-in user can gild the submission.
    ``can_mod_post``                  Whether the logged-in user can modify the post.
    ``category``                      The submission's category.
    ``clicked``                       Whether the submission has been clicked by the logged-in user previously.
    ``content_categories``            The content categories assigned to the submission.
    ``contest_mode``                  Whether the moderators of the subreddit have enabled contest mode on
                                      the submission.
    ``created_utc``                   The parsed UTC ``datetime`` on which the submission was made.
    ``created``                       The timestamp of when the submission was posted.
    ``discussion_type``               ``null``
    ``distinguished``                 The type of distinguishment on the submission.
    ``domain``                        The domain of the submission.
    ``downs``                         The number of downvotes on the submission.
    ``edited``                        Whether the submission has been edited by its author.
    ``gilded``                        The number of awards this submission has received.
    ``gildings``                      The gild awards the submission has received.
    ``hidden``                        Whether the submission has been hidden by the logged-in user.
    ``hide_score``                    Whether clients should hide the score from users.
    ``id``                            The submission's ID.
    ``ignore_reports``                Whether reports should be ignored on this submission.``
    ``is_crosspostable``              Whether the submission can be crossposted to other subreddits.
    ``is_meta``                       Whether the submission is a meta post.
    ``is_original_content``           Whether the submission has been marked as original content.
    ``is_reddit_media_domain``        Whether the media has been uploaded to Reddit.
    ``is_robot_indexable``            Whether the submission can be indexed by robots.
    ``is_self``                       Whether the submission is a self post.
    ``is_video``                      Whether the submission is a video post.
    ``likes``                         ``bool``
    ``link_flair_background_color``   The submission's flair background color.
    ``link_flair_css_class``          The CSS class applied on the submission's flair if applicable.
    ``link_flair_richtext``           The submission's flair text if applicable.
    ``link_flair_template_id``        The submission's flair template ID if applicable.
    ``link_flair_text_color``         The submission's flair text color if applicable.
    ``link_flair_text``               The submission's flair text.
    ``link_flair_type``               The type of flair applied to the submission.
    ``locked``                        Whether the submission has been locked by the subreddit moderators.
    ``media_embed``                   ``Dict``
    ``media_only``                    Whether the submission only consists of media.
    ``media``                         ``null``
    ``mod_note``                      Moderator notes added to the submission.
    ``mod_reason_by``                 The moderator who added the removal reason if applicable.
    ``mod_reason_title``              The reason the submission has been removed by moderators if applicable.
    ``mod_reports``                   A list of moderator reports on the submission.
    ``name``                          The ID of the submission prepended with ``t3_``.
    ``no_follow``                     ``bool``
    ``num_comments``                  The number of comments on the submission.
    ``num_crossposts``                The number of times the submission has been crossposted.
    ``num_reports``                   The number of reports on the submission.
    ``over_18``                       Whether the submission has been marked as NSFW.
    ``parent_whitelist_status``       ``null``
    ``permalink``                     The submission's permalink.
    ``pinned``                        Whether the submission has been pinned on the subreddit.
    ``pwls``                          ``null``
    ``quarantine``                    Whether the submission was posted in a quarantined subreddit.
    ``removal_reason``                The submission's removal reason if applicable.
    ``removed``                       Whether the submission has been removed by the subreddit moderators.
    ``report_reasons``                A list of report reasons on the submission.
    ``saved``                         Whether the submission has been saved by the logged-in user.
    ``score``                         The overall submission vote score.
    ``secure_media_embed``            ``Dict``
    ``secure_media``                  ``null``
    ``selftext_html``                 The submission text as HTML.
    ``selftext``                      The submission's selftext.
    ``send_replies``                  Whether the author of the submission will receive reply notifications.
    ``spam``                          Whether the submission has been marked as spam.
    ``spoiler``                       Whether the submission contains a spoiler.
    ``stickied``                      Whether the submission is stickied on the subreddit.
    ``subreddit_id``                  The subreddit's ID prepended with ``t5_``.
    ``subreddit_name_prefixed``       The name of the subreddit the submission was posted on, prefixed with "r/".
    ``subreddit_subscribers``         The number of subscribers to the submission's subreddit.
    ``subreddit_type``                The type of the subreddit the submission was posted on
                                      (public, restricted, private).
    ``subreddit``                     The name of the subreddit on which the submission was posted.
    ``suggested_sort``                The suggested sort method for comments.
    ``thumbnail_height``              The height of the submission's thumbnail if applicable.
    ``thumbnail_width``               The width of the submission's thumbnail if applicable.
    ``thumbnail``                     A URL to the submission's thumbnail if applicable.
    ``title``                         The submission's title.
    ``total_awards_received``         The number of awards on the submission.
    ``ups``                           The number of upvotes on the submission.
    ``url``                           The full URL of the submission.
    ``user_reports``                  A list of the user reports on the submission.
    ``view_count``                    The number of views on the submission.
    ``visited``                       Whether the logged-in user has visited the submission previously.
    ``whitelist_status``              ``null``
    ``wls``                           ``null``
    ================================= ============================================================================

    .. note::
        Many of these attributes are only available if the logged-in user has moderator access to the item.

    """

    def __init__(self, reddit: 'Reddit', data: Dict, subreddit: Subreddit = None, author: Redditor = None):
        """
        Create an instance of a submission object.

        Parameters
        ----------
        reddit: Reddit
            The :class:`~apraw.Reddit` instance with which requests are made.
        data: Dict
            The data obtained from the /about endpoint.
        full_data: Dict
            The full_data retrieved by the /r/{sub}/comments/{id} endpoint.
        subreddit: Subreddit
            The subreddit this submission was posted on.
        author: Redditor
            The author of this submission as a :class:`~apraw.models.Redditor`.
        """
        self.comments = list()

        aPRAWBase.__init__(self, reddit, data, reddit.link_kind)
        AuthorMixin.__init__(self, author)
        SubredditMixin.__init__(self, subreddit)

        self.mod = SubmissionModeration(reddit, self)

    async def fetch(self):
        """
        Fetch this item's information from a suitable API endpoint.

        Returns
        -------
        self: Submission
            The updated model.
        """
        if "subreddit" in self._data and "id" in self._data:
            resp = await self._reddit.get(
                API_PATH["submission"].format(sub=self._data["subreddit"], id=self._data["id"]))
            self._update(resp)
        elif "id" in self._data:
            resp = await self._reddit.get(API_PATH["info"],
                                          id=prepend_kind(self._data["id"], self._reddit.link_kind))
            self._update(resp["data"]["children"][0]["data"])
        return self

    def _update(self, _data: Union[List, Dict[str, Any]]):
        """
        Update the base with new information.

        Parameters
        ----------
        _data: Dict
            The data obtained from the API.
        """
        if isinstance(_data, dict) or isinstance(_data, list):
            if isinstance(_data, dict):
                data = _data
            else:
                from ..helpers.comment_forest import CommentForest
                self.comments = CommentForest(self._reddit, _data[1]["data"], self.fullname)
                data = _data[0]["data"]["children"][0]

            data["original_content"] = data.get("is_original_content", False)
            super()._update(data)
        else:
            raise ValueError("data is not of type 'dict' or 'list'.")


class SubmissionModeration(PostModeration, NSFWableMixin, SpoilerableMixin):
    """
    A helper class to moderate submissions.
    """

    def __init__(self, reddit: 'Reddit', submission: Submission):
        """
        Create an instance of ``SubmissionModeration``.

        Parameters
        ----------
        reddit : Reddit
            The :class:`~apraw.Reddit` instance with which requests are made.
        submission : Submission
            The submission this helper performs requests for.
        """
        super().__init__(reddit, submission)

    async def sticky(self, position: int = 1, to_profile: bool = False):
        """
        Sticky a submission in its subreddit.

        Parameters
        ----------
        position : int
            The "slot" the submission will be stickied to.
        to_profile : bool
            Whether the submission will be stickied to the user profile.

        Returns
        -------
        resp: Dict
            The API response JSON.
        """
        return await self._reddit.post(API_PATH["mod_sticky"], **{
            "id": self.fullname,
            "num": position,
            "state": True,
            "to_profile": to_profile
        })

    async def unsticky(self, to_profile: bool = False):
        """
        Unsticky a submission from its subreddit.

        Parameters
        ----------
        to_profile : bool
            Whether the submission will be unstickied from the user profile.

        Returns
        -------
        resp: Dict
            The API response JSON.
        """
        return await self._reddit.post(API_PATH["mod_sticky"], **{
            "id": self.fullname,
            "state": False,
            "to_profile": to_profile
        })
