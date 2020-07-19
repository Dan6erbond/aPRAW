from typing import TYPE_CHECKING, Dict

from ..reddit.comment import Comment
from ..reddit.listing import Listing
from ..reddit.more_comments import MoreComments
from ..subreddit.subreddit import Subreddit

if TYPE_CHECKING:
    from ...reddit import Reddit


class CommentForest(Listing):
    """
    ``CommentForest`` is an iterable used by :class:`~apraw.models.Comment` and :class:`~apraw.models.Submission`
    containing the replies and comment threads. The items can be iterated over just like any other listing, which could
    contain either :class:`~apraw.models.Comment` or :class:`~apraw.models.MoreComments`.
    """

    def __init__(self, reddit: 'Reddit', data: Dict, link_id: str, subreddit: Subreddit = None):
        super().__init__(reddit, data, subreddit, link_id=link_id)
        self._comments_unfolded = []

    async def replace_more(self):
        """
        Replaces all the :class:`~apraw.models.MoreComments` instances with the comments they reference.

        This method can be used to retrieve all the comments, and only comments within a forest. This task could take a
        while for larger threads, after which the comment forest can be iterated over and all the comments with their
        replies will be made available.
        """
        if not self._comments_unfolded:
            for item in self:
                if isinstance(item, MoreComments):
                    comments = await item.comments()
                    for comment in comments:
                        if comment.replies:
                            await comment.replies.replace_more()
                    self._comments_unfolded.extend(comments)
                elif isinstance(item, Comment):
                    if item.replies:
                        await item.replies.replace_more()
                    self._comments_unfolded.append(item)

            setattr(self, self.CHILD_ATTRIBUTE, self._comments_unfolded)
