import pytest
import json
from headbot.client import HeadbotAsyncClient, HeadbotAsyncClientException
from headbot.settings import API_ROOT_URL


TEST_EMAIL = "vasya.pupkin@gmail.com"
TEST_PASSWORD = "abc123"


class TestHeadbotAsyncClient:

    @pytest.mark.asyncio
    async def test_client_auth_by_email_and_password_exception(
            self, aioresponses):
        aioresponses.post(
            f"{API_ROOT_URL}token/", status=401, body=json.dumps({
                "detail": "No active account found with the given credentials"
            }))
        with pytest.raises(HeadbotAsyncClientException) as e_info:
            async with HeadbotAsyncClient(
                    email=TEST_EMAIL, password=TEST_PASSWORD):
                pass
        assert str(e_info.value) == "Authorization (token/) failed"

    @pytest.mark.asyncio
    async def test_client_auth_by_refresh_token_exception(self, aioresponses):
        aioresponses.post(
            f"{API_ROOT_URL}token/", status=200, body=json.dumps({
                "access": "some_access_token",
                "refresh": "some_refresh_token"
            }))
        aioresponses.post(
            f"{API_ROOT_URL}token/refresh/", status=401, body=json.dumps({
                "detail": "No active account found with the given credentials"
            }))
        async with HeadbotAsyncClient(
                email=TEST_EMAIL, password=TEST_PASSWORD) as client:
            with pytest.raises(HeadbotAsyncClientException) as e_info:
                await client.auth_by_refresh_token(
                    refresh_token="wrong_referesh_token")                
        assert str(e_info.value) == "Authorization (token/refresh/) failed"

    @pytest.mark.asyncio
    async def test_client_auth_by_email_and_password(self, aioresponses):
        aioresponses.post(
            f"{API_ROOT_URL}token/", status=200, body=json.dumps({
                "access": "some_access_token",
                "refresh": "some_refresh_token"
            }))
        async with HeadbotAsyncClient(
                email=TEST_EMAIL, password=TEST_PASSWORD) as client:
            assert client.access_token
            assert client.refresh_token

    @pytest.mark.asyncio
    async def test_client_crawler_list(self, aioresponses):
        aioresponses.post(
            f"{API_ROOT_URL}token/", status=200, body=json.dumps({
                "access": "some_access_token",
                "refresh": "some_refresh_token"
            }))
        aioresponses.get(
            f"{API_ROOT_URL}crawlers/", status=200, body=json.dumps([
                {"name": "My First Crawler"}
            ]))
        async with HeadbotAsyncClient(
                email=TEST_EMAIL, password=TEST_PASSWORD) as client:
            crawlers = await client.crawlers()
            assert isinstance(crawlers, list)
            assert len(crawlers) == 1
            for crawler in crawlers:
                assert isinstance(crawler, dict)
                assert "name" in crawler
                assert isinstance(crawler["name"], str)

    @pytest.mark.asyncio
    async def test_client_token_expiration(self, aioresponses):
        aioresponses.post(
            f"{API_ROOT_URL}token/", status=200, body=json.dumps({
                "access": "some_access_token",
                "refresh": "some_refresh_token"
            }))
        aioresponses.get(
            f"{API_ROOT_URL}crawlers/", status=401, body=json.dumps({
                "detail": "Given token not valid for any token type",
                "code": "token_not_valid",
                "messages": [{
                    "token_class": "AccessToken",
                    "token_type": "access",
                    "message": "Token is invalid or expired"
                }]
            }))
        aioresponses.post(
            f"{API_ROOT_URL}token/refresh/", status=200, body=json.dumps({
                "access": "another_access_token",
                "refresh": "another_refresh_token"
            }))
        aioresponses.get(
            f"{API_ROOT_URL}crawlers/", status=200, body=json.dumps([
                {"name": "My First Crawler"}
            ]))
        async with HeadbotAsyncClient(
                email=TEST_EMAIL, password=TEST_PASSWORD) as client:
            # let's pretend that the access token is expired...
            crawlers = await client.crawlers()
            assert client.access_token == "another_access_token"
            assert client.refresh_token == "another_refresh_token"
            assert isinstance(crawlers, list)
            assert len(crawlers) == 1
            for crawler in crawlers:
                assert isinstance(crawler, dict)
                assert "name" in crawler
                assert isinstance(crawler["name"], str)
