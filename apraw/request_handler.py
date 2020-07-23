import asyncio
from datetime import datetime, timedelta
from functools import wraps
from typing import Dict, Callable, Any, Awaitable, Optional

from multidict import CIMultiDictProxy

from .const import BASE_URL
from .models import User


class RequestHandler:

    def __init__(self, user: User):
        self.user = user
        self.queue = []

    async def get_request_headers(self) -> Dict:
        if self.user.token_expires <= datetime.now():
            url = "https://www.reddit.com/api/v1/access_token"
            session = await self.user.auth_session()

            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": self.user.user_agent
            }

            resp = await session.post(url, data=self.user.password_grant, headers=headers)

            async with resp:
                if resp.status == 200:
                    self.user.access_data = await resp.json()
                    self.user.token_expires = datetime.now(
                    ) + timedelta(seconds=self.user.access_data["expires_in"])
                else:
                    raise Exception("Invalid user data.")

        return {
            "Authorization": "{} {}".format(self.user.access_data["token_type"], self.user.access_data["access_token"]),
            "User-Agent": self.user.user_agent
        }

    def update(self, data: CIMultiDictProxy):
        if "x-ratelimit-remaining" in data:
            self.user.ratelimit_remaining = int(float(data["x-ratelimit-remaining"]))
        if "x-ratelimit-used" in data:
            self.user.ratelimit_used = int(data["x-ratelimit-used"])
        if "x-ratelimit-reset" in data:
            self.user.ratelimit_reset = datetime.now() + timedelta(seconds=int(data["x-ratelimit-reset"]))

    async def close(self):
        await self.user.close()

    class Decorators:

        @classmethod
        def check_ratelimit(
                cls, func: Callable[[Any, Any], Awaitable[Any]]) -> Callable[[Any, Any], Awaitable[Any]]:
            @wraps(func)
            async def execute_request(self, *args, **kwargs) -> Any:
                id = datetime.now().strftime('%Y%m%d%H%M%S')
                self.queue.append(id)

                if self.user.ratelimit_remaining < 1:
                    execution_time = self.user.ratelimit_reset + \
                                     timedelta(seconds=len(self.queue))
                    wait_time = (execution_time - datetime.now()).total_seconds()
                    await asyncio.sleep(wait_time)

                result = await func(self, *args, **kwargs)
                self.queue.remove(id)
                return result

            return execute_request

    @Decorators.check_ratelimit
    async def get(self, endpoint: Optional[str] = "", _url: Optional[str] = "", **kwargs) -> Any:
        kwargs = {"raw_json": 1, "api_type": "json", **kwargs}
        params = ["{}={}".format(k, kwargs[k]) for k in kwargs]

        if endpoint:
            url = BASE_URL.format(endpoint, "&".join(params))
        elif _url:
            url = _url + "?" + "&".join(params)
        else:
            raise ValueError("One of endpoint or _url must be specified.")

        headers = await self.get_request_headers()
        session = await self.user.client_session()
        resp = await session.get(url, headers=headers)

        async with resp:
            self.update(resp.headers)
            return await resp.json()

    @Decorators.check_ratelimit
    async def delete(self, endpoint: str = "", **kwargs) -> Any:
        kwargs = {"raw_json": 1, "api_type": "json", **kwargs}
        params = ["{}={}".format(k, kwargs[k]) for k in kwargs]

        url = BASE_URL.format(endpoint, "&".join(params))

        headers = await self.get_request_headers()
        session = await self.user.client_session()
        resp = await session.delete(url, headers=headers)

        async with resp:
            self.update(resp.headers)
            return await resp.json()

    @Decorators.check_ratelimit
    async def put(self, endpoint: str = "", data: Dict = None, **kwargs) -> Any:
        kwargs = {"raw_json": 1, "api_type": "json", **kwargs}
        params = ["{}={}".format(k, kwargs[k]) for k in kwargs]

        url = BASE_URL.format(endpoint, "&".join(params))

        headers = await self.get_request_headers()
        session = await self.user.client_session()
        resp = await session.delete(url, data=data, headers=headers)

        async with resp:
            self.update(resp.headers)
            return await resp.json()

    @Decorators.check_ratelimit
    async def post(self, endpoint: str = "", url: str = "", data: Dict = None, **kwargs) -> Any:
        kwargs = {"raw_json": 1, "api_type": "json", **kwargs}
        params = ["{}={}".format(k, kwargs[k]) for k in kwargs]

        if endpoint:
            url = BASE_URL.format(endpoint, "&".join(params))
        elif url:
            url = "{}?{}".format(url, "&".join(params))

        headers = await self.get_request_headers()
        session = await self.user.client_session()
        resp = await session.post(url, data=data, headers=headers)

        async with resp:
            self.update(resp.headers)
            return await resp.json()
