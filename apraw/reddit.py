from datetime import datetime
from datetime import timedelta

import configparser
import aiohttp

from .subreddits import Subreddits
from .subreddit import Subreddit
from .redditor import Redditor


class Reddit:

    def __init__(self, praw_key="", username="", password="", client_id="", client_secret="", user_agent="aPRAW by Dan6erbond"):
        if praw_key != "":
            config = configparser.ConfigParser()
            config.read("praw.ini")
            self.username = config[praw_key]["username"]
            self.password = config[praw_key]["password"]
            self.client_id = config[praw_key]["client_id"]
            self.client_secret = config[praw_key]["client_secret"]
            self.user_agent = config[praw_key]["user_agent"] if "user_agent" in config[praw_key] else user_agent
        else:
            self.username = username
            self.password = password
            self.client_id = client_id
            self.client_secret = client_secret
            self.user_agent = user_agent

        if self.username == "" or self.password == "" or self.client_id == "" or self.client_secret == "":
            raise Exception("No login info given.")

        self.comment_kind = "t1"
        self.account_kind = "t2"
        self.link_kind = "t3"
        self.message_kind = "t4"
        self.subreddit_kind = "t5"
        self.award_kind = "t6"

        self.subreddits = Subreddits(self)

        self.access_data = None
        self.token_expires = datetime.now()

    async def get_request_headers(self):
        if self.token_expires <= datetime.now():
            url = "https://www.reddit.com/api/v1/access_token"
            data = {
                "grant_type": "password",
                "username": self.username,
                "password": self.password
            }

            auth = aiohttp.BasicAuth(login=self.client_id, password=self.client_secret)
            async with aiohttp.ClientSession(auth=auth) as session:
                async with session.post(url, data=data) as resp:
                    if resp.status == 200:
                        self.access_data = await resp.json()
                        self.token_expires = datetime.now() + timedelta(seconds=self.access_data["expires_in"])
                    else:
                        raise Exception("Invalid user data.")

        return {
            "Authorization": "{} {}".format(self.access_data["token_type"], self.access_data["access_token"]),
            "User-Agent": self.user_agent
        }

    async def get_request(self, endpoint, **kwargs):
        kwargs["raw_json"] = 1
        params = ["{}={}".format(k, kwargs[k]) for k in kwargs]
        url = "https://oauth.reddit.com{}?{}".format(endpoint, "&".join(params))

        async with aiohttp.ClientSession() as session:
            headers = await self.get_request_headers()
            async with session.get(url, headers=headers) as resp:
                return await resp.json()

    async def get_listing(self, endpoint, limit, **kwargs):
        last = None
        while True:
            kwargs["limit"] = limit if limit is not None else 100
            if last is not None:
                kwargs["after"] = last
            req = await self.get_request(endpoint, **kwargs)
            if len(req["data"]["children"]) <= 0:
                break
            for i in req["data"]["children"]:
                if i["kind"] in [self.link_kind, self.subreddit_kind]:
                    last = i["data"]["name"]
                if limit is not None: limit -= 1
                yield i
            if limit is not None and limit < 1:
                break

    async def post_request(self, endpoint, data, **kwargs):
        kwargs["raw_json"] = 1
        params = ["{}={}".format(k, kwargs[k]) for k in kwargs]
        url = "https://oauth.reddit.com{}?{}".format(endpoint, "&".join(params))

        async with aiohttp.ClientSession() as session:
            headers = await self.get_request_headers()
            async with session.post(url, data=data, headers=headers) as resp:
                return await resp.json()

    async def subreddit(self, display_name):
        resp = await self.get_request("/r/{}/about".format(display_name))
        try:
            return Subreddit(self, resp["data"])
        except Exception as e:
            # print("No Subreddit data loaded from:", resp)
            return None

    async def redditor(self, username):
        resp = await self.get_request("/user/{}/about".format(username))
        try:
            return Redditor(self, resp["data"])
        except Exception as e:
            # print("No Redditor data loaded for {}.".format(username))
            return None

    async def message(self, to, subject, text, from_sr=""):
        data = {
            "subject": subject,
            "text": text,
            "to": to
        }
        if from_sr != "": data["from_sr"] = from_sr
        resp = await self.post_request("/api/compose", data)
        return resp["success"]