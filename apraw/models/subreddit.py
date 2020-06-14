import asyncio
from datetime import datetime

from ..endpoints import API_PATH
from .comment import Comment
from .modmail import SubredditModmail
from .submission import Submission


class Subreddit:
    def __init__(self, reddit, data):
        self.reddit = reddit
        self.data = data
        self.mod = SubredditModeration(self)
        self.modmail = SubredditModmail(self)

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

        from .listing_generator import ListingGenerator
        self.comments = ListingGenerator(
            self.reddit, API_PATH["subreddit_comments"].format(
                sub=self.display_name))
        self.new = ListingGenerator(self.reddit,
                                    API_PATH["subreddit_new"].format(sub=self.display_name))
        self.hot = ListingGenerator(self.reddit,
                                    API_PATH["subreddit_hot"].format(sub=self.display_name))
        self.rising = ListingGenerator(
            self.reddit, API_PATH["subreddit_rising"].format(sub=self.display_name))
        self.top = ListingGenerator(self.reddit,
                                    API_PATH["subreddit_top"].format(sub=self.display_name))

    def __str__(self):
        return self.display_name

    async def moderators(self, **kwargs):
        req = await self.reddit.get_request(API_PATH["subreddit_moderators"].format(sub=self.display_name), **kwargs)
        for u in req["data"]["children"]:
            yield SubredditModerator(self.reddit, u)

    async def message(self, subject, text, from_sr=""):
        return await self.reddit.message(API_PATH["subreddit"].format(sub=self.display_name), subject, text, from_sr)


class SubredditStream():
    def __init__(self, subreddit):
        self.subreddit = subreddit

    async def comments(self):
        # TODO: implement
        pass

    async def submissions(self, max_wait=16, **kwargs):
        wait = 0
        ids = list()

        while True:
            found = False
            async for s in self.subreddit.new(100, **kwargs):
                if s.id in ids:
                    break
                if len(ids) >= 301:
                    ids = ids[1:]
                ids.append(s.id)
                found = True
                yield s

            if found:
                wait = 1
            else:
                wait *= 2
                if wait > max_wait:
                    wait = 1

            print(wait)
            await asyncio.sleep(wait)


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
        async for s in self.subreddit.reddit.get_listing(API_PATH["subreddit_reports"].format(sub=self.subreddit.display_name),
                                                         limit, **kwargs):
            if s["kind"] == self.subreddit.reddit.link_kind:
                yield Submission(self.subreddit.reddit, s["data"], subreddit=self.subreddit)
            elif s["kind"] == self.subreddit.reddit.comment_kind:
                yield Comment(self.subreddit.reddit, s["data"])

    async def spam(self, limit=25, **kwargs):
        async for s in self.subreddit.reddit.get_listing(API_PATH["subreddit_spam"].format(sub=self.subreddit.display_name),
                                                         limit, **kwargs):
            if s["kind"] == self.subreddit.reddit.link_kind:
                yield Submission(self.subreddit.reddit, s["data"], subreddit=self.subreddit)
            elif s["kind"] == self.subreddit.reddit.comment_kind:
                yield Comment(self.subreddit.reddit, s["data"])

    async def modqueue(self, limit=25, **kwargs):
        async for s in self.subreddit.reddit.get_listing(API_PATH["subreddit_modqueue"].format(sub=self.subreddit.display_name),
                                                         limit, **kwargs):
            if s["kind"] == self.subreddit.reddit.link_kind:
                yield Submission(self.subreddit.reddit, s["data"], subreddit=self.subreddit)
            elif s["kind"] == self.subreddit.reddit.comment_kind:
                yield Comment(self.subreddit.reddit, s["data"])

    async def unmoderated(self, limit=25, **kwargs):
        async for s in self.subreddit.reddit.get_listing(API_PATH["subreddit_unmoderated"].format(sub=self.subreddit.display_name),
                                                         limit, **kwargs):
            if s["kind"] == self.subreddit.reddit.link_kind:
                yield Submission(self.subreddit.reddit, s["data"], subreddit=self.subreddit)
            elif s["kind"] == self.subreddit.reddit.comment_kind:
                yield Comment(self.subreddit.reddit, s["data"])

    async def edited(self, limit=25, **kwargs):
        async for s in self.subreddit.reddit.get_listing(API_PATH["subreddit_edited"].format(sub=self.subreddit.display_name),
                                                         limit, **kwargs):
            if s["kind"] == self.subreddit.reddit.link_kind:
                yield Submission(self.subreddit.reddit, s["data"], subreddit=self.subreddit)
            elif s["kind"] == self.subreddit.reddit.comment_kind:
                yield Comment(self.subreddit.reddit, s["data"])

    async def log(self, limit=25, **kwargs):
        async for l in self.subreddit.reddit.get_listing(API_PATH["subreddit_log"].format(sub=self.subreddit.display_name),
                                                         limit, **kwargs):
            yield ModAction(l["data"], self.subreddit)


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
