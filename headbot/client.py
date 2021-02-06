import asyncio
from aiohttp import ClientSession
from typing import Optional, Type
from types import TracebackType
from .settings import API_ROOT_URL


class HeadbotClientException:
    pass


class HeadbotClient:
    """
    """

    def __init__(self, email: str, password: str) -> None:
        self.session = None
        self.email = email
        self.password = password
        # self.token = None
        # self.refresh_token = None

    async def __aenter__(self) -> "HeadbotClient":
        self.session = ClientSession()
        return self

    async def close(self) -> None:
        await self.session.close()

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self.close()

    async def crawlers(self):
        return []

    # async def auth(self):
    #     pass

    # async def refresh_token(self):
    #     pass
