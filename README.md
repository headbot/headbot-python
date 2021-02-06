# Headbot.io Python Client

Python client for the [headbot.io API](http://headbot.io/api/).

## Installing
```
pip install headbot
```

## Supported versions
* Python 3.6+

## Usage
```
import asyncio
from pprint import pprint
from headbot.client import HeadbotClient


async def main():
    async with HeadbotClient(email="{email}", password="{password}") as client:
        my_crawlers = await client.crawlers()
        pprint(my_crawlers)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop = loop.run_until_complete(main())

```
