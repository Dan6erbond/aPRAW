import asyncio
from datetime import datetime
from typing import TYPE_CHECKING, Dict, List, Any, Union

from reactive import all_reactive, ReactiveOwner

from .redditor import Redditor
from ..helpers.apraw_base import aPRAWBase
from ..helpers.item_moderation import PostModeration
from ..mixins.author import AuthorMixin
from ..mixins.deletable import DeletableMixin
from ..mixins.hideable import HideableMixin
from ..mixins.replyable import ReplyableMixin
from ..mixins.savable import SavableMixin
from ..mixins.subreddit import SubredditMixin
from ..mixins.votable import VotableMixin
from ..subreddit.subreddit import Subreddit
from ...const import API_PATH
from ...utils import prepend_kind, snake_case_keys, ExponentialCounter

if TYPE_CHECKING:
    from ...reddit import Reddit
    from .submission import Submission
    from ..helpers.comment_forest import CommentForest


@all_reactive(not_type=(aPRAWBase, datetime, PostModeration))
class Comment(aPRAWBase, DeletableMixin, HideableMixin, ReplyableMixin, SavableMixin, VotableMixin, AuthorMixin,
              SubredditMixin, ReactiveOwner):
    """
    The model representing comments.

    Members
    -------
    mod: CommentModeration
        The :class:`~apraw.models.CommentModeration` instance to aid in moderating the comment.
    kind: str
        The item's kind / type.
    url: str
        The URL pointing to this comment.

    **Typical Attributes**

    This table describes attributes that typically belong to objects of this
    class. Attributes are dynamically provided by the :class:`~apraw.models.aPRAWBase` class
    and may vary depending on the status of the response and expected objects.

    ================================= ===========================================================================
    Attribute                         Description
    ================================= ===========================================================================
    ``all_awardings``                 A list of awardings added to the comment.
    ``approved_at_utc``               The UTC timestamp at which the comment was approved by the moderators.
    ``approved_by``                   The moderator who approved this comment if applicable.
    ``approved``                      Whether the comment has been approved by the moderators.
    ``archived``                      Whether the comment has been archived.
    ``author_flair_background_color`` The comment author's flair background color if applicable.
    ``author_flair_css_class``        The comment author's flair CSS class if applicable.
    ``author_flair_richtext``         The comment author's flair text if applicable.
    ``author_flair_template_id``      The comment author's flair template ID if applicable.
    ``author_flair_text_color``       The comment author's flair text color if applicable.
    ``author_flair_text``             The comment author's flair text if applicable.
    ``author_flair_type``             The comment author's flair type if applicable.
    ``author_fullname``               The comment author's ID prepended with ``t2_``.
    ``author_patreon_flair``          The comment author's Patreon flair if applicable.
    ``author``                        The comment author's username.
    ``banned_at_utc``                 ``None``
    ``banned_by``                     ``None``
    ``body_html``                     The HTML version of the comment's body.
    ``body``                          The comment's markdown body.
    ``can_gild``                      Whether the logged-in user can gild the comment.
    ``can_mod_post``                  ``bool``
    ``collapsed_reason``              ``None``
    ``collapsed``                     Whether the comment should be collapsed by clients.
    ``controversiality``              A score on the comment's controversiality based on its up- and downvotes.
    ``created_utc``                   The parsed UTC ``datetime`` on which the comment was made.
    ``created``                       A timestamp on which the comment was created.
    ``distinguished``                 The type of distinguishment the comment hsa received.
    ``downs``                         The number of downvotes the comment has received.
    ``edited``                        Whether the comment has been edited from its original state.
    ``gilded``                        The number of awards this comment has received.
    ``gildings``                      A dictionary of gilds the comment has received.
    ``id``                            The comment's ID.
    ``ignore_reports``                Whether reports should be ignored on this comment.
    ``is_submitter``                  Whether the logged-in user is the submitter of this comment.
    ``likes``                         The overall upvote score on this comment.
    ``link_author``                   The username of the comment submission's author.
    ``link_id``                       The ID of the submission this comment was made in.
    ``link_permalink`` / ``link_url`` A URL to the comment's submission.
    ``link_title``                    The comment's submission title.
    ``locked``                        Whether the comment has been locked by the moderators.
    ``mod_note``                      Notes added to the comment by moderators if applicable.
    ``mod_reason_by``                 The moderator who added a removal reason if applicable.
    ``mod_reason_title``              The mod reason's title if applicable.
    ``mod_reports``                   A list of reports made on this comment filed by moderators.
    ``name``                          The comment's ID prepended with ``t1_``.
    ``no_follow``                     ``bool``
    ``num_comments``                  The number of replies made in this submission.
    ``num_reports``                   The number of reports on this comment.
    ``over_18``                       Whether the comment has been marked NSFW.
    ``parent_id``                     The comment's parent ID, either ``link_id`` or the ID of another comment.
    ``permalink``                     The comment's permalink.
    ``quarantine``                    ``bool``
    ``removal_reason``                A removal reason set by moderators if applicable.
    ``removed``                       Whether the comment has been removed by the moderators of the subreddit.
    ``replies``                       A list of replies made under this comment, usually empty at first.
    ``report_reasons``                Report reasons added to the comment.
    ``saved``                         Whether the logged-in user has saved this comment.
    ``score_hidden``                  Whether clients should hide the comment's score.
    ``score``                         The overall upvote score on this comment.
    ``send_replies``                  Whether the OP has enabled reply notifications.
    ``spam``                          Whether the comment has been flagged as spam.
    ``stickied``                      Whether the comment has been stickied by the moderators.
    ``subreddit_id``                  The comment subreddit's ID prepended with ``t5_``.
    ``subreddit_name_prefixed``       The comment's subreddit name prefixed with "r/".
    ``subreddit_type``                The type of the subreddit the submission was posted on
                                      (public, restricted, private).
    ``subreddit``                     The name of the subreddit this comment was made in.
    ``total_awards_received``         The number of awards this comment has received.
    ``ups``                           The number of upvotes this comment has received.
    ``user_reports``                  A list of user reports filed for this comment.
    ================================= ===========================================================================

    .. note::
        Many of these attributes are only available if the logged-in user has moderator access to the item.

    """

    def __init__(self, reddit: 'Reddit', data: Dict, submission: 'Submission' = None,
                 author: Redditor = None, subreddit: Subreddit = None, replies: Union['CommentForest', List] = None):
        """
        Create an instance of a comment.

        Parameters
        ----------
        reddit: Reddit
            The :class:`~apraw.Reddit` instance with which requests are made.
        data: Dict
            The data obtained from the /about endpoint.
        submission: Submission
            The submission this comment was made in as a :class:`~apraw.models.Submission`.
        author: Redditor
            The author of this comment as a :class:`~apraw.models.Redditor`.
        subreddit: Subreddit
            The subreddit this comment was made in as a :class:`~apraw.models.Subreddit`.
        replies: List[Comment]
            A list of replies made to this comment.
        """
        self.replies = replies if replies else []

        ReactiveOwner.__init__(self)
        aPRAWBase.__init__(self, reddit, data, reddit.comment_kind)
        AuthorMixin.__init__(self, author)
        SubredditMixin.__init__(self, subreddit)

        self._submission = submission
        self.mod = CommentModeration(reddit, self)

    async def fetch(self):
        """
        Fetch this item's information from a suitable API endpoint.

        Returns
        -------
        self: Comment
            The ``Comment`` model with updated data.
        """
        if ("link_id" in self._data and "id" in self._data and "subreddit" in self._data) or "permalink" in self._data:
            permalink = self._data["permalink"] if "permalink" in self._data else API_PATH["comment"].format(
                sub=self._data["subreddit"], submission=self._data["link_id"].replace(self._reddit.link_kind + "_", ""),
                id=self._data["id"])
            resp = await self._reddit.get_request(permalink)
            from .submission import Submission
            self._submission = Submission(self._reddit, resp[0]["data"]["children"][0]["data"])
            return self._update(resp[1]["data"]["children"][0]["data"])
        elif "id" in self._data:
            resp = await self._reddit.get_request(API_PATH["info"],
                                                  id=prepend_kind(self._data["id"], self._reddit.comment_kind))
            return self._update(resp["data"]["children"][0]["data"])
        else:
            raise ValueError(f"No data available to make request URL: {self._data}")

    async def monitor(self, max_wait=16):
        counter = ExponentialCounter(max_wait)
        while True:
            updates = await self.fetch()
            if updates:
                wait = counter.reset()
            else:
                wait = counter.count()
            await asyncio.sleep(wait)

    def _update(self, _data: Union[List, Dict[str, Any]]):
        """
        Update the base with new information.

        Parameters
        ----------
        _data: Dict
            The data obtained from the API.
        """

        if isinstance(_data, dict) or isinstance(_data, list):
            data = _data if isinstance(_data, dict) else _data[0]["data"]
            if isinstance(_data, list):
                from ..helpers.comment_forest import CommentForest
                self.replies = CommentForest(self._reddit, _data[1]["data"], data["link_id"])

            self._data = data

            d = snake_case_keys(data)
            if "created_utc" in d:
                d["created_utc"] = datetime.utcfromtimestamp(d["created_utc"])
            self._data_attrs.update([k for k in d if not hasattr(self, k)])
            updates = [{"name": k, "value": v} for (k, v) in d.items() if not hasattr(self, k) or k in self._data_attrs]

            if "link_id" in d and "id" in d and "subreddit" in d:
                link_id = d["link_id"].replace(self._reddit.link_kind + "_", "")
                url = API_PATH["comment"].format(sub=d["subreddit"], submission=link_id, id=d["id"])
                updates.append({"name": "url", "value": url})
            elif "permalink" in d:
                url = "https://www.reddit.com" + d["permalink"]
                updates.append({"name": "url", "value": url})

            return self._bulk_update(*updates)
        else:
            raise TypeError("data is not of type 'dict' or 'list'.")

    async def submission(self) -> 'Submission':
        """
        Retrieve the submission this comment was made in as a :class:`~apraw.models.Submission`.

        Returns
        -------
        submission: Submission
            The submission this comment was made in.
        """
        if self._submission is None:
            link = await self._reddit.get_request(API_PATH["info"], id=self._data["link_id"])
            from .submission import Submission
            self._submission = Submission(
                self._reddit, link["data"]["children"][0]["data"])
        return self._submission


class CommentModeration(PostModeration):
    """
    A helper class to moderate comments.

    Members
    -------
    reddit: Reddit
        The :class:`~apraw.Reddit` instance with which requests are made.
    fullname: str
        The ID prepended with the kind of the item this helper belongs to.
    """

    def __init__(self, reddit: 'Reddit', comment: Comment):
        """
        Create an instance of ``CommentModeration``.

        Parameters
        ----------
        reddit : Reddit
            The :class:`~apraw.Reddit` instance with which requests are made.
        comment : Comment
            The comment this helper performs requests for.
        """
        super().__init__(reddit, comment)

    async def show_comment(self):
        """
        Mark a comment that it should not be collapsed because of crowd control.

        The comment could still be collapsed for other reasons.

        Returns
        -------
        resp: Dict
            The API response JSON.
        """
        return await self.reddit.post_request(API_PATH["mod_show_comment"], id=self.fullname)
