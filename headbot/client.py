import logging
import json
from typing import Optional, Type, List, Dict, Tuple, Union, Any
from types import TracebackType
from aiohttp import ClientSession
from .settings import API_ROOT_URL


logger = logging.getLogger(__name__)


class HeadbotAsyncClientException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class HeadbotAsyncClient:
    """
    Asynchronous client for the headbot.io API.
    """

    def __init__(self, email: str, password: str) -> None:
        self.email = email
        self.password = password
        self.session = None
        self.access_token = None
        self.refresh_token = None

    async def auth_by_payload(
            self, api_segment: str, payload: Dict[str, str]) -> Tuple[str, str]:
        """
        Authorizes the client by a payload and recieves acess/refresh tokens
        :param api_segment: an API segment to request;
        :param payload: a dictionary with the request parameters;
        :return: a tuple (access token & refresh token).
        """
        headers = {"Content-Type": "application/json"}
        payload = json.dumps(payload)
        async with self.session.post(
                f"{API_ROOT_URL}{api_segment}",
                data=payload,
                headers=headers) as response:
            logger.debug(f"Response Status: {response.status}")
            if response.status == 200:
                data = await response.json()
                return data["access"], data["refresh"]
            elif response.status == 401:
                logger.debug(await response.text())
                await self.close()
                raise HeadbotAsyncClientException(
                    f"Authorization ({api_segment}) failed")

    async def auth_by_email_and_password(
            self, email: str, password: str) -> Tuple[str, str]:
        """
        Authorizes the client by an email/password pair and recieves 
        access/refresh tokens.
        :param email: email to pass;
        :param password: password to pass;
        :return: a tuple (access token & refresh token).
        """
        payload = {"email": email, "password": password}
        return await self.auth_by_payload(api_segment="token/", payload=payload)

    async def auth_by_refresh_token(
            self, refresh_token: str) -> Tuple[str, str]:
        """
        Authorizes the client by a refresh token and recieves access/refresh 
        tokens.
        :param refresh_token: a refresh token;
        :return: a tuple (access token & refresh token).
        """
        payload = {"refresh": refresh_token}
        return await self.auth_by_payload(
            api_segment="token/refresh/", payload=payload)

    async def __aenter__(self) -> "HeadbotAsyncClient":
        self.session = ClientSession()
        self.access_token, self.refresh_token = \
            await self.auth_by_email_and_password(
                email=self.email, password=self.password)
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

    async def request(self, api_segment: str, method: str = "GET") -> Union[
            List[Dict[str, Any]], Dict[str, Any]]:
        """
        Performs a request to the headbot.io API.
        :param api_segment: an API segment to request;
        :param method: an HTTP method (GET/POST/PUT/DELETE);
        :return: a response.
        """
        # if not self.access_token or not self.refresh_token:
        #     self.access_token, self.refresh_token = \
        #         await self.auth_by_email_and_password(
        #             email=self.email, password=self.password)
        headers = {"Authorization": f"Bearer {self.access_token}"}
        if method == "GET":
            api_method = self.session.get
        else:
            api_method = self.session.post
        async with api_method(
                f"{API_ROOT_URL}{api_segment}", headers=headers) as response:
            logger.debug(f"Response Status: {response.status}")
            if response.status == 200:
                return await response.json()
            elif response.status == 401:
                logger.debug(await response.text())
                self.access_token, self.refresh_token = \
                    await self.auth_by_refresh_token(
                        refresh_token=self.refresh_token)
                return await self.request(
                    api_segment=api_segment, method=method)

    async def crawlers(self) -> List[Dict[str, Any]]:
        """
        Retrieves all crawlers associated with the current user.
        """
        return await self.request(api_segment="crawlers/")

    # async def crawler_runs(self) -> List[Dict[str, Any]]:
    #     """
    #     Retrieves all crawler runs associated with the current user.
    #     """
    #     return await self.request(api_segment="crawler_runs/")
