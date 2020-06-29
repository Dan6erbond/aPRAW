from typing import TYPE_CHECKING, Dict, List, Union

from ..endpoints import API_PATH
from .helpers.apraw_base import aPRAWBase
from .redditor import Redditor

if TYPE_CHECKING:
    from ..reddit import Reddit
    from .subreddit import Subreddit


class SubredditWiki:

    def __init__(self, subreddit: 'Subreddit'):
        self.subreddit = subreddit

        self._data = None

        from .helpers.listing_generator import ListingGenerator
        self.revisions = ListingGenerator(
            subreddit.reddit, API_PATH["wiki_revisions"].format(
                sub=self.subreddit))

    async def data(self, refresh=False) -> Dict:
        if self._data is None:
            self._data = await self.subreddit.reddit.get_request(
                API_PATH["wiki"].format(sub=self.subreddit))
        return self._data

    async def __call__(self) -> List[str]:
        data = await self.data()
        return [page for page in data["data"]]

    async def page(self, page: str) -> 'SubredditWikipage':
        resp = await self.subreddit.reddit.get_request(
            API_PATH["wiki_page"].format(sub=self.subreddit, page=page))
        return SubredditWikipage(page, self.subreddit, resp["data"])

    async def create(self, page: str, content_md: str = "", reason: str = "") -> 'SubredditWikipage':
        resp = await self.subreddit.reddit.post_request(
            API_PATH["wiki_edit"].format(sub=self.subreddit), data={
                "page": page,
                "content": content_md,
                "reason": reason
            })
        return resp if resp else await self.page(page)


class SubredditWikipage(aPRAWBase):

    def __init__(self, name: str, subreddit: 'Subreddit', data: Dict = None):
        super().__init__(subreddit.reddit, data, subreddit.reddit.wikipage_kind)

        self.name = name
        self.subreddit = subreddit

        from .helpers.listing_generator import ListingGenerator
        self.revisions = ListingGenerator(
            subreddit.reddit, API_PATH["wiki_page_revisions"].format(
                sub=self.subreddit, page=self.name))

    async def _alloweditor(self, username: str, act: str):
        resp = await self.subreddit.reddit.post_request(
            API_PATH["wiki_alloweditor"].format(sub=self.subreddit, act=act), data={
                "page": self.name,
                "username": username
            })
        return True if not resp else resp

    async def add_editor(self, username: str):
        return await self._alloweditor(username, "add")

    async def del_editor(self, username: str):
        return await self._alloweditor(username, "del")

    async def edit(self, content_md: str = "", reason: str = "") -> bool:
        resp = await self.subreddit.reddit.post_request(
            API_PATH["wiki_edit"].format(sub=self.subreddit), data={
                "page": self.name,
                "content": content_md,
                "reason": reason
            })
        return resp if resp else True

    async def hide(self, revision: Union[str, 'WikipageRevision']):
        resp = await self.subreddit.reddit.post_request(
            API_PATH["wiki_hide"].format(sub=self.subreddit), data={
                "page": self.name,
                "revision": str(revision)
            })
        return resp if resp else True

    async def revert(self, revision: Union[str, 'WikipageRevision']):
        resp = await self.subreddit.reddit.post_request(
            API_PATH["wiki_revert"].format(sub=self.subreddit), data={
                "page": self.name,
                "revision": str(revision)
            })
        return resp if resp else True


class WikipageRevision(aPRAWBase):

    def __init__(self, reddit: 'Reddit', data: Dict = None):
        super().__init__(reddit, data, reddit.wiki_revision_kind)

        self.author = Redditor(reddit, data["author"]["data"])

    def __str__(self):
        return self.id
