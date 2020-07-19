from typing import TYPE_CHECKING, Dict, Any, List, Union

from .comment import Comment
from .submission import Submission
from ..helpers.apraw_base import aPRAWBase
from ..mixins.link import LinkMixin
from ...const import API_PATH

if TYPE_CHECKING:
    from ...reddit import Reddit


class MoreComments(aPRAWBase, LinkMixin):
    """
    Represents the model for more comments in a thread.

    **Typical Attributes**

    This table describes attributes that typically belong to objects of this
    class. Attributes are dynamically provided by the :class:`~apraw.models.aPRAWBase` class
    and may vary depending on the status of the response and expected objects.

    ============= ================================================================
    Attribute     Description
    ============= ================================================================
    ``count``     The number of comment or more children items in this thread.
    ``name``      The fullname that references this more comments model.
    ``id``        The ID of this more comments model.
    ``parent_id`` The ID of this more comments' parent submission or comment.
    ``depth``     The depth this more comments model goes into.
    ``children``  A list of comment and more comment IDs available in this thread.
    ============= ================================================================

    """

    def __init__(self, reddit: 'Reddit', data: Dict[str, Any], link_id: str):
        """
        Create an instance of ``MoreComments``.

        Parameters
        ----------
        reddit: Reddit
            The :class:`~apraw.Reddit` instance with which requests are made.
        data: Dict
            The data obtained from the /about endpoint.
        link_id: str
            The ID of the submission this ``MoreComments`` instance belongs to.
            This needs to be known for the ``MoreComments`` instance to be able to fetch its comments.
        """
        data.update(link_id=link_id)
        super().__init__(reddit, data)

        self._comments = []
        self._ids = list(self.children)
        self._index = 0

    async def _next_batch(self):
        """
        Retrieve the next batch of :class:`~apraw.models.Comment` and further ``MoreComments`` in this thread.
        These will be added to the internal list and can be read by using the instance as a generator or fetching the
        comments with :func:`~apraw.models.MoreComments.comments`.
        """
        if not self._ids:
            return

        ids = self._ids[:100]
        self._ids = self._ids[100:]
        resp = await self._reddit.get(API_PATH["morechildren"], **{
            "children": ",".join(ids),
            "link_id": self.link_id,
            "id": self.id,
            "depth": self.depth
        })

        from .listing import MoreChildren
        children = MoreChildren(self._reddit, resp["json"]["data"], [self._reddit.comment_kind, self._reddit.more_kind],
                                self.link_id)
        self._comments.extend(comment for comment in children)

    async def parent(self) -> Union[Submission, Comment]:
        """
        Retrieve the parent submission or comment of this MoreComments object.

        Returns
        -------
        parent: Submission or Comment
            The parent submission or comment of this MoreComments object.
        """
        return await self._reddit.info(self.parent_id)

    async def fetch(self):
        """
        Fetch all the comments in this MoreComments thread.
        """
        while self._ids:
            await self._next_batch()

    def __aiter__(self):
        """
        Permit ``MoreComments`` to operate as an iterator.

        Returns
        -------
        self: MoreComments
            The iterator.
        """
        return self

    async def __anext__(self) -> Comment:
        """
        Permit ``MoreComments`` to operate as a generator.

        Returns the next comment in the listing.

        Returns
        -------
        comment: Comment
            The next comment in the list.

        Raises
        ------
        StopAsyncIteration
            Raised once the list of comments has been exhausted.
        """
        if self._index >= len(self._comments) and not self._ids:
            raise StopAsyncIteration

        if not self._comments or self._ids:
            await self._next_batch()

        self._index += 1
        return self._comments[self._index + 1]

    async def comments(self) -> List[Union[Comment, 'MoreComments']]:
        """
        Retrieve a list of all the :class:`~apraw.models.Comment` and further ``MoreComments`` in this thread.

        Returns
        -------
        comments: List[Union[Comment, MoreComments]]
            A list of all the :class:`~apraw.models.Comment` and further ``MoreComments`` in this thread.
        """
        if not self._comments:
            await self.fetch()

        return self._comments
