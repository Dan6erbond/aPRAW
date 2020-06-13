from datetime import datetime

from .subreddit import Subreddit
from .submission import Submission
from .comment import Comment

class Redditor:
    def __init__(self, reddit, data):
        self.reddit = reddit
        self.data = data

        self.name = data["name"]

        if "is_suspended" not in data or not data["is_suspended"]:
            self.id = data["id"]
            self.is_suspended = False
            self.created_utc = datetime.utcfromtimestamp(data["created_utc"])

            self.is_employee = data["is_employee"]
            # self.has_visited_new_profile = data["has_visited_new_profile"]
            self.is_friend = data["is_friend"]
            # self.pref_no_profanity = data["pref_no_profanity"]
            # self.has_external_account = data["has_external_account"]
            # self.is_sponsor = data["is_sponsor"]
            # self.has_gold_subscription = data["has_gold_subscription"]
            # self.num_friends = data["num_friends"]
            self.verified = data["verified"]
            # self.over18 = data["over_18"] if "over18" in data else data["subreddit"]["over_18"] if "over_18" in data["subreddit"] else False
            self.is_gold = data["is_gold"]
            self.is_mod = data["is_mod"]
            self.has_verified_email = data["has_verified_email"]
            # self.pref_video_autoplay = data["pref_video_autoplay"]
            # self.in_chat = data["in_chat"]
            # self.in_redesign_beta = data["in_redesign_beta"]
            # self.pref_nightmode = data["pref_nightmode"]

            self.link_karma = data["link_karma"]
            self.comment_karma = data["comment_karma"]
        else:
            self.is_suspended = True

        if "subreddit" in data and data["subreddit"] is not None:
            sub = data["subreddit"]
            sub["id"] = sub["name"].replace("t5_", "")
            if "created_utc" not in sub: sub["created_utc"] = data["created_utc"]
            # sub["over18"] = self.over18
            self.subreddit = Subreddit(self.reddit, sub)
        else:
            self.subreddit = None

    def __str__(self):
        return self.name

    async def moderated_subreddits(self, **kwargs):
        req = await self.reddit.get_request("/user/{}/moderated_subreddits".format(self), **kwargs)
        for s in req["data"]:
            yield await self.reddit.subreddit(s["sr"])

    async def message(self, subject, text, from_sr=""):
        return await self.reddit.message(self.name, subject, text, from_sr)

    async def comments(self, limit=25, **kwargs):
        async for s in self.reddit.get_listing("/user/{}/comments".format(self.name), limit, **kwargs):
            if s["kind"] == self.reddit.comment_kind:
                yield Comment(self.reddit, s["data"])

    async def submissions(self, limit=25, **kwargs):
        async for s in self.reddit.get_listing("/user/{}/submitted".format(self.name), limit, **kwargs):
            if s["kind"] == self.reddit.link_kind:
                yield Submission(self.reddit, s["data"])