# Headbot.io Python Client

[![Build Status](https://travis-ci.org/headbot/headbot-python.svg?branch=master)](https://travis-ci.org/headbot/headbot-python)
[![Build Status](https://img.shields.io/pypi/v/headbot.svg?color=blue)](https://pypi.org/project/headbot/)
[![pypi supported versions](https://img.shields.io/pypi/pyversions/headbot.svg)](https://pypi.python.org/pypi/headbot)

Python client for the [headbot.io API](http://headbot.io/api/).

## Installing
```
pip install headbot
```

## Supported versions
* Python 3.6+

## Usage
```python
import asyncio
from pprint import pprint
from headbot.client import HeadbotAsyncClient


async def main():
    async with HeadbotAsyncClient(
            email="{email}",
            password="{password}"
            ) as client:
        my_crawlers = await client.crawlers()
        pprint(my_crawlers)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop = loop.run_until_complete(main())

```
