import aiohttp

from .subreddit import Subreddit


class Subreddits:

    def __init__(self, reddit):
        self.reddit = reddit

    async def new(self, limit=25, **kwargs):
        async for s in self.reddit.get_listing("/subreddits/new", limit, **kwargs):
            if s["kind"] == self.reddit.subreddit_kind:
                yield Subreddit(self.reddit, s["data"])
