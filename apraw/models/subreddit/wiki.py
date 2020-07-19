from typing import TYPE_CHECKING, Dict, List, Union, Any, Optional

from ..helpers.apraw_base import aPRAWBase
from ..helpers.streamable import streamable
from ..reddit.redditor import Redditor
from ...const import API_PATH

if TYPE_CHECKING:
    from ...reddit import Reddit
    from .subreddit import Subreddit


class SubredditWiki:
    """
    A helper class to aid in retrieving subreddit wiki pages, revisions as well as creating items.
    """

    def __init__(self, reddit: 'Reddit', subreddit: 'Subreddit'):
        """
        Create an instance of ``SubredditWiki``.

        Parameters
        ----------
        reddit: Reddit
            The :class:`~apraw.Reddit` instance with which requests are made.
        subreddit: Subreddit
            The subreddit this helper performs requests for.
        """
        self._reddit = reddit
        self._subreddit = subreddit
        self._data = None

    #: Streamable listing endpoint.
    @streamable
    def revisions(self, *args, **kwargs):
        r"""
        Returns an instance of :class:`~apraw.models.ListingGenerator` mapped to recent wikipage revisions.

        .. note::
            This listing can be streamed doing the following:

            .. code-block:: python3

                for comment in subreddit.wiki.stream():
                    print(comment)

        Parameters
        ----------
        kwargs: \*\*Dict
            :class:`~apraw.models.ListingGenerator` ``kwargs``.

        Returns
        -------
        generator: ListingGenerator
            A :class:`~apraw.models.ListingGenerator` mapped to recent wikipage revisions.
        """
        from ..helpers.generator import ListingGenerator
        return ListingGenerator(self._reddit, API_PATH["wiki_revisions"].format(sub=self._subreddit), *args,
                                **kwargs)

    async def _fetch(self) -> Dict:
        """
        Fetch the data for a subreddit's wiki from the API.
        """
        url = API_PATH["wiki"].format(sub=self._subreddit)
        self._data = await self._reddit.get(url)
        return self._data

    async def __call__(self) -> List[str]:
        """
        Retrieve a list of the available wikipages.

        Returns
        -------
        pages: List[str]
            A list of all the wikipages in the subreddit by name.
        """
        if not self._data:
            await self._fetch()
        return [page for page in self._data["data"]]

    async def page(self, page: str) -> 'SubredditWikipage':
        """
        Retrieve a specific :class:`~apraw.models.SubredditWikipage` by its name.

        Parameters
        ----------
        page: str
            The wikipage's name which can be retrieved using the list from
            :func:`~apraw.models.SubredditWiki.__call__()`.

        Returns
        -------
        wikipage: SubredditWikipage
            The requested wikipage if it exists.
        """
        url = API_PATH["wiki_page"].format(sub=self._subreddit, page=page)
        resp = await self._reddit.get(url)
        return SubredditWikipage(page, self._reddit, self._subreddit, resp["data"])

    async def create(self, page: str, content_md: str = "", reason: str = "") -> 'SubredditWikipage':
        """
        Create a new wikipage on the subreddit.

        Parameters
        ----------
        page: str
            The wikipage's name.
        content_md: str
            The wikipage's content as a markdown string.
        reason: str
            An optional string detailing the reason for the creation of this wikipage.

        Returns
        -------
        wikipage: SubredditWikipage
            The newly created wikipage.
        """
        resp = await self._reddit.post(
            API_PATH["wiki_edit"].format(sub=self._subreddit), data={
                "page": page,
                "content": content_md,
                "reason": reason
            })
        return resp if resp else await self.page(page)


class SubredditWikipage(aPRAWBase):
    """
    The model that represents Subreddit wikipages.

    **Typical Attributes**

    This table describes attributes that typically belong to objects of this
    class. Attributes are dynamically provided by the :class:`~apraw.models.aPRAWBase` class
    and may vary depending on the status of the response and expected objects.

    ================= =============================================================
    Attribute         Description
    ================= =============================================================
    ``content_html``  The content's of the wikipage as an HTML string.
    ``content_md``    The content's of the wikipage formatted as a markdown string.
    ``may_revise``    ``bool``
    ``name``          The wikipage's name.
    ``reason``        The reason text for the wikipage's current revision.
    ``revision_by``   The author of the wikipage's current revision.
    ``revision_date`` The date on which the current revision was made.
    ``revision_id``   The ID of the wikipage's current revision.
    ================= =============================================================
    """

    def __init__(self, name: str, reddit: 'Reddit', subreddit: 'Subreddit', data: Dict = None):
        """
        Create an instance of ``SubredditWikipage``.

        Parameters
        ----------
        name: str
            The wikipage's name.
        reddit: Reddit
            The :class:`~apraw.Reddit` instance with which requests are made.
        subreddit: Subreddit
            The subreddit this helper performs requests for.
        data: Dict
            The data returned by the API endpoint.
        """
        super().__init__(reddit, data, reddit.wikipage_kind)

        self.name = name
        self._subreddit = subreddit

    #: Streamable listing endpoint.
    @streamable
    def revisions(self, *args, **kwargs):
        r"""
        Returns an instance of :class:`~apraw.models.ListingGenerator` mapped to fetch specific wikipage revisions.

        .. note::
            This listing can be streamed doing the following:

            .. code-block:: python3

                for comment in subreddit.wiki.page("test").stream():
                    print(comment)

        Parameters
        ----------
        kwargs: \*\*Dict
            :class:`~apraw.models.ListingGenerator` ``kwargs``.

        Returns
        -------
        generator: ListingGenerator
            A :class:`~apraw.models.ListingGenerator` mapped to fetch specific wikipage revisions.
        """
        from ..helpers.generator import ListingGenerator
        return ListingGenerator(self._reddit, API_PATH["wiki_page_revisions"].format(
            sub=self._subreddit, page=self.name), *args, **kwargs)

    async def _alloweditor(self, username: str, act: str):
        """
        Remove or add a Redditor from the editors of this wikipage.

        Parameters
        ----------
        username: str
            The Redditor's username without the prefix.
        act: str
            Either "add" or "del" based on the act to be performed.

        Returns
        -------
        res: bool or Any
            ``True`` if the request was successful, otherwise the response's raw data.
        """
        resp = await self._reddit.post(
            API_PATH["wiki_alloweditor"].format(sub=self._subreddit, act=act), data={
                "page": self.name,
                "username": username
            })
        return True if not resp else resp

    async def add_editor(self, username: str) -> Union[bool, Any]:
        """
        Add a Redditor to the editors of this wikipage.

        Parameters
        ----------
        username: str
            The Redditor's username without the prefix.

        Returns
        -------
        res: bool or Any
            ``True`` if the request was successful, otherwise the response's raw data.
        """
        return await self._alloweditor(username, "add")

    async def del_editor(self, username: str) -> Union[bool, Any]:
        """
        Remove a Redditor from the editors of this wikipage.

        Parameters
        ----------
        username: str
            The Redditor's username without the prefix.

        Returns
        -------
        res: bool or Any
            ``True`` if the request was successful, otherwise the response's raw data.
        """
        return await self._alloweditor(username, "del")

    async def edit(self, content_md: str, reason: Optional[str] = "") -> Union[bool, Any]:
        """
        Edit a wikipage's markdown contents.

        Parameters
        ----------
        content_md: str
            The new wikipage's content as a markdown string.
        reason: Optional[str]
            An optional reason for this edit.

        Returns
        -------
        res: bool or Any
            ``True`` if the request was successful, otherwise the response's raw data.
        """
        resp = await self._reddit.post(
            API_PATH["wiki_edit"].format(sub=self._subreddit), data={
                "page": self.name,
                "content": content_md,
                "reason": reason
            })
        return resp if resp else True

    async def hide(self, revision: Union[str, 'WikipageRevision']):
        """
        Hide a wikipage revision from the public history.

        Parameters
        ----------
        revision: str or WikipageRevision
            The wikipage revision either as a :class:`~apraw.models.WikipageRevision` or its ID string.

        Returns
        -------
        res: bool or Any
            ``True`` if the request was successful, otherwise the response's raw data.
        """
        resp = await self._reddit.post(
            API_PATH["wiki_hide"].format(sub=self._subreddit), data={
                "page": self.name,
                "revision": str(revision)
            })
        return resp if resp else True

    async def revert(self, revision: Union[str, 'WikipageRevision']) -> Union[bool, Any]:
        """
        Revert a wikipage to its previous revision.

        Parameters
        ----------
        revision: str or WikipageRevision
            The wikipage revision either as a :class:`~apraw.models.WikipageRevision` or its ID string.

        Returns
        -------
        res: bool or Any
            ``True`` if the request was successful, otherwise the response's raw data.
        """
        resp = await self._reddit.post(
            API_PATH["wiki_revert"].format(sub=self._subreddit), data={
                "page": self.name,
                "revision": str(revision)
            })
        return resp if resp else True


class WikipageRevision(aPRAWBase):
    """
    The model that represents wikipage revisions.

    Members
    -------
    author: Redditor
        The Redditor that made this revision.

    **Typical Attributes**

    This table describes attributes that typically belong to objects of this
    class. Attributes are dynamically provided by the :class:`~apraw.models.aPRAWBase` class
    and may vary depending on the status of the response and expected objects.

    =================== ====================================================
    Attribute           Description
    =================== ====================================================
    ``timestamp``       A timestamp of when the revision was made.
    ``page``            The name of the page the revision addresses.
    ``revision_hidden`` Whether the revision has been hidden by the editors.
    ``reason``          The reason string for this revision if available.
    ``id``              The ID of this revision.
    =================== ====================================================
    """

    def __init__(self, reddit: 'Reddit', data: Dict = None):
        """
        Create an instance of ``WikipageRevision``.

        Parameters
        ----------
        reddit: Reddit
            The :class:`~apraw.Reddit` instance with which requests are made.
        data: Dict
            The data returned by the API endpoint.
        """
        super().__init__(reddit, data, reddit.wiki_revision_kind)

        self.author = Redditor(reddit, data["author"]["data"])

    def __str__(self):
        """
        Retrieve the string representation of this object.

        Returns
        -------
        id: str
            The ID of this wikipage revision.
        """
        return self.id
