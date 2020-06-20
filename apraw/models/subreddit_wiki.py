from typing import TYPE_CHECKING, Dict, List

from ..endpoints import API_PATH
from .apraw_base import aPRAWBase
from .redditor import Redditor

if TYPE_CHECKING:
    from ..reddit import Reddit
    from .subreddit import Subreddit


class SubredditWiki:

    def __init__(self, subreddit: 'Subreddit'):
        self.subreddit = subreddit

        self._data = None

        from .listing_generator import ListingGenerator
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

    async def page(self, page: str) -> 'SubredditWikiPage':
        resp = await self.subreddit.reddit.get_request(
            API_PATH["wiki_page"].format(sub=self.subreddit, page=page))
        return SubredditWikiPage(self.subreddit, resp["data"])


class SubredditWikiPage(aPRAWBase):

    def __init__(self, subreddit: 'Subreddit', data: Dict = None):
        super().__init__(subreddit.reddit, data)

        self.subreddit = subreddit


class WikiPageRevision(aPRAWBase):

    def __init__(self, reddit: 'Reddit', data: Dict = None):
        super().__init__(reddit, data)

        self.author = Redditor(reddit, data["author"]["data"])
