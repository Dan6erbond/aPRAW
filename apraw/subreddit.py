import asyncio
from datetime import datetime

from .comment import Comment
from .modmail import SubredditModmail
from .submission import Submission


class Subreddit:
    def __init__(self, reddit, data):
        self.reddit = reddit
        self.data = data
        self.mod = SubredditModeration(self)
        self.modmail = SubredditModmail(self)
        self.stream = SubredditStream(self)

        self.id = data["id"]
        self.created_utc = datetime.utcfromtimestamp(data["created_utc"])

        self.display_name = data["display_name"]
        self.public_description = data["public_description"]
        self.description = data["description"]
        self.subscribers = data["subscribers"]
        self.quarantine = data["quarantine"] if "quarantine" in data else False
        self.subreddit_type = data["subreddit_type"]
        self.over18 = data["over18"] if "over18" in data else data["over_18"] if "over_18" in data else False
        self.user_is_subscribed = data["user_is_subscriber"]
        self.user_is_moderator = data["user_is_moderator"]

    def __str__(self):
        return self.display_name

    async def comments(self, limit=25, **kwargs):
        # TODO: implement
        pass

    async def new(self, limit=25, **kwargs):
        async for s in self.reddit.get_listing("/r/{}/new".format(self.display_name), limit, **kwargs):
            if s["kind"] == self.reddit.link_kind:
                yield Submission(self.reddit, s["data"], subreddit=self)

    async def moderators(self, **kwargs):
        req = await self.reddit.get_request("/r/{}/about/moderators".format(self.display_name), **kwargs)
        for u in req["data"]["children"]:
            yield SubredditModerator(self.reddit, u)

    async def message(self, subject, text, from_sr=""):
        return await self.reddit.message("/r/" + self.display_name, subject, text, from_sr)


class SubredditStream():
    def __init__(self, subreddit):
        self.subreddit = subreddit

    async def comments(self):
        # TODO: implement
        pass

    async def submissions(self, limit=100, max_wait=15, **kwargs):
        while True:
            wait = 0
            ids = list()

            found = False
            async for s in self.subreddit.new(limit, **kwargs):
                if s.id in ids:
                    break
                ids.append(s.id)
                found = True
                yield s

            ids = ids[:100]

            if found:
                wait = 0

            await asyncio.sleep(wait)

            if not found:
                wait += 1
                if wait > max_wait:
                    wait = 0


class SubredditModerator():
    def __init__(self, reddit, data):
        self.reddit = reddit
        self.data = data

        self.id = data["id"]

        self.name = data["name"]
        self.author_flair_text = data["author_flair_text"]
        self.author_flair_css_class = data["author_flair_css_class"]
        self.mod_permissions = data["mod_permissions"]
        self.added = data["date"]

    def __str__(self):
        return self.name

    async def redditor(self):
        return await self.reddit.redditor(self.name)


class SubredditModeration:
    def __init__(self, subreddit):
        self.subreddit = subreddit

    async def reports(self, limit=25, **kwargs):
        async for s in self.subreddit.reddit.get_listing("/r/{}/about/reports".format(self.subreddit.display_name),
                                                         limit, **kwargs):
            if s["kind"] == self.subreddit.reddit.link_kind:
                yield Submission(self.subreddit.reddit, s["data"], subreddit=self.subreddit)
            elif s["kind"] == self.subreddit.reddit.comment_kind:
                yield Comment(self.subreddit.reddit, s["data"])

    async def spam(self, limit=25, **kwargs):
        async for s in self.subreddit.reddit.get_listing("/r/{}/about/spam".format(self.subreddit.display_name),
                                                         limit, **kwargs):
            if s["kind"] == self.subreddit.reddit.link_kind:
                yield Submission(self.subreddit.reddit, s["data"], subreddit=self.subreddit)
            elif s["kind"] == self.subreddit.reddit.comment_kind:
                yield Comment(self.subreddit.reddit, s["data"])

    async def modqueue(self, limit=25, **kwargs):
        async for s in self.subreddit.reddit.get_listing("/r/{}/about/modqueue".format(self.subreddit.display_name),
                                                         limit, **kwargs):
            if s["kind"] == self.subreddit.reddit.link_kind:
                yield Submission(self.subreddit.reddit, s["data"], subreddit=self.subreddit)
            elif s["kind"] == self.subreddit.reddit.comment_kind:
                yield Comment(self.subreddit.reddit, s["data"])

    async def unmoderated(self, limit=25, **kwargs):
        async for s in self.subreddit.reddit.get_listing("/r/{}/about/unmoderated".format(self.subreddit.display_name),
                                                         limit, **kwargs):
            if s["kind"] == self.subreddit.reddit.link_kind:
                yield Submission(self.subreddit.reddit, s["data"], subreddit=self.subreddit)
            elif s["kind"] == self.subreddit.reddit.comment_kind:
                yield Comment(self.subreddit.reddit, s["data"])

    async def edited(self, limit=25, **kwargs):
        async for s in self.subreddit.reddit.get_listing("/r/{}/about/edited".format(self.subreddit.display_name),
                                                         limit, **kwargs):
            if s["kind"] == self.subreddit.reddit.link_kind:
                yield Submission(self.subreddit.reddit, s["data"], subreddit=self.subreddit)
            elif s["kind"] == self.subreddit.reddit.comment_kind:
                yield Comment(self.subreddit.reddit, s["data"])

    async def log(self, limit=25, **kwargs):
        async for l in self.subreddit.reddit.get_listing("/r/{}/about/log".format(self.subreddit.display_name),
                                                         limit, **kwargs):
            print(ModAction(l["data"], self.subreddit))


class ModAction:
    def __init__(self, data, subreddit=None):
        self.data = data
        self.subreddit = subreddit

        self.id = data["id"]

        self.created_utc = datetime.utcfromtimestamp(data["created_utc"])

        self.mod = data["mod"]
        self.description = data["description"]
        self.details = data["details"]
        self.action = data["action"]

        self.target_body = data["target_body"]
        self.target_title = data["target_title"]
        self.target_permalink = data["target_permalink"]
        self.target_author = data["target_author"]
        self.target_fullname = data["target_fullname"]

    async def mod(self):
        return await self.subreddit.reddit.redditor(self.mod)
