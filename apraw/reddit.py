import asyncio
import configparser
import logging
from datetime import datetime, timedelta
from typing import Any, Awaitable, Callable, Dict, List, Union

import aiohttp

from .endpoints import API_PATH, BASE_URL
from .models import (Comment, ListingGenerator, Redditor, Submission,
                     Subreddit, User)
from .utils import prepend_kind


class Reddit:

    def __init__(self, praw_key: str = "", username: str = "", password: str = "",
                 client_id: str = "", client_secret: str = "",
                 user_agent="aPRAW by Dan6erbond"):
        if praw_key != "":
            config = configparser.ConfigParser()
            config.read("praw.ini")

            self.user = User(self, config[praw_key]["username"], config[praw_key]["password"],
                             config[praw_key]["client_id"], config[praw_key]["client_secret"],
                             config[praw_key]["user_agent"] if "user_agent" in config[praw_key] else user_agent)
        else:
            self.user = User(self, username, password,
                             client_id, client_secret, user_agent)

        self.comment_kind = "t1"
        self.account_kind = "t2"
        self.link_kind = "t3"
        self.message_kind = "t4"
        self.subreddit_kind = "t5"
        self.award_kind = "t6"
        self.modaction_kind = "modaction"
        self.listing_kind = "Listing"
        self.wiki_revision_kind = "WikiRevision"

        self.subreddits = ListingGenerator(self, API_PATH["subreddits_new"])
        self.request_handler = RequestHandler(self.user)

    async def get_request(self, *args, **kwargs):
        return await self.request_handler.get_request(*args, **kwargs)

    async def post_request(self, *args, **kwargs):
        return await self.request_handler.post_request(*args, **kwargs)

    def get_listing_generator(self, *args, **kwargs):
        return ListingGenerator.get_listing_generator(self, *args, **kwargs)

    async def subreddit(self, display_name: str) -> Subreddit:
        resp = await self.get_request(API_PATH["subreddit_about"].format(sub=display_name))
        try:
            return Subreddit(self, resp["data"])
        except Exception as e:
            logging.error(e)
            return None

    async def info(self, id: str = "", ids: List[str] = [], url: str = ""):
        listing_generator = self.get_listing_generator(API_PATH["info"])

        if id:
            async for i in listing_generator(id=id):
                yield i
        elif ids:
            async for i in listing_generator(None, id=",".join(ids)):
                yield i
        elif url:
            async for i in listing_generator(url=url):
                yield i
        else:
            yield None

    async def submission(self, id: str = "", url: str = "") -> Submission:
        if id != "":
            async for link in self.info(prepend_kind(id, self.link_kind)):
                return link
        elif url != "":
            async for link in self.info(url=url):
                return link
        return None

    async def comment(self, id: str = "", url: str = "") -> Comment:
        if id != "":
            async for comment in self.info(prepend_kind(id, self.comment_kind)):
                return comment
        elif url != "":
            async for comment in self.info(url=url):
                return comment
        return None

    async def redditor(self, username: str) -> Redditor:
        resp = await self.get_request(API_PATH["user_about"].format(user=username))
        try:
            return Redditor(self, resp["data"])
        except Exception as e:
            # print("No Redditor data loaded for {}.".format(username))
            return None

    async def message(self, to: Union[str, Redditor], subject: str, text: str, from_sr: Union[str, Subreddit] = "") -> Dict:
        data = {
            "subject": subject,
            "text": text,
            "to": str(to)
        }
        if from_sr != "":
            data["from_sr"] = str(from_sr)
        resp = await self.post_request(API_PATH["compose"], data=data)
        return resp["success"]


class RequestHandler:

    def __init__(self, user):
        self.user = user
        self.queue = []

    async def get_request_headers(self) -> Dict:
        if self.user.token_expires <= datetime.now():
            url = "https://www.reddit.com/api/v1/access_token"
            session = self.user.get_auth_session()

            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": self.user.user_agent
            }

            resp = await session.post(url, data=self.user.password_grant, headers=headers)

            async with resp:
                if resp.status == 200:
                    self.user.access_data = await resp.json()
                    self.user.token_expires = datetime.now()
                    + timedelta(seconds=self.user.access_data["expires_in"])
                else:
                    raise Exception("Invalid user data.")

        return {
            "Authorization": "{} {}".format(self.user.access_data["token_type"], self.user.access_data["access_token"]),
            "User-Agent": self.user.user_agent
        }

    def update(self, data: Dict):
        self.user.ratelimit_remaining = int(
            float(data["x-ratelimit-remaining"]))
        self.user.ratelimit_used = int(data["x-ratelimit-used"])

        self.user.ratelimit_reset = datetime.now()
        + timedelta(seconds=int(data["x-ratelimit-reset"]))

    def check_ratelimit(
            func: Callable[[Any], Awaitable[Any]]) -> Callable[[Any], Awaitable[Any]]:
        async def execute_request(self, *args, **kwargs) -> Any:
            id = datetime.now().strftime('%Y%m%d%H%M%S')
            self.queue.append(id)

            if (self.user.ratelimit_remaining < 5):
                execution_time = self.user.ratelimit_reset
                + timedelta(seconds=len(self.queue))
                wait_time = (execution_time - datetime.now()).total_seconds()
                await asyncio.sleep(wait_time)

            result = await func(self, *args, **kwargs)
            self.queue.remove(id)
            return result

        return execute_request

    @check_ratelimit
    async def get_request(self, endpoint: str = "", **kwargs) -> Dict:
        kwargs["raw_json"] = 1
        params = ["{}={}".format(k, kwargs[k]) for k in kwargs]

        url = BASE_URL.format(endpoint, "&".join(params))

        headers = await self.get_request_headers()
        session = self.user.get_client_session()
        resp = await session.get(url, headers=headers)

        async with resp:
            self.update(resp.headers)
            return await resp.json()

    @check_ratelimit
    async def post_request(self, endpoint: str = "", url: str = "", data: Dict = {}, **kwargs) -> Dict:
        kwargs["raw_json"] = 1
        params = ["{}={}".format(k, kwargs[k]) for k in kwargs]

        if endpoint != "":
            url = BASE_URL.format(endpoint, "&".join(params))
        elif url != "":
            url = "{}?{}".format(url, "&".join(params))

        headers = await self.get_request_headers()
        session = self.user.get_client_session()
        resp = await session.post(url, data=data, headers=headers)

        async with resp:
            self.update(resp.headers)
            return await resp.json()
