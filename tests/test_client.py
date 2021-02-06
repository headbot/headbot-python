import pytest
from headbot.client import HeadbotClient, HeadbotClientException


TEST_EMAIL = "vasya.pupkin@gmail.com"
TEST_PASSWORD = "abc123"


@pytest.mark.asyncio
async def test_client():
    async with HeadbotClient(
            email=TEST_EMAIL, password=TEST_PASSWORD) as client:
        await client.crawlers()
