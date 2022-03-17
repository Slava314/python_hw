import asyncio
import time
import aiohttp
from random import randint
import requests


async def download_picture(url, session, num):
    async with session.get(url) as response:
        content = await response.read()
        with open('artifacts/picture' + str(num) + '.png', 'wb') as f:
            f.write(content)


async def download_all_pictures(pictures):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url, num in pictures:
            task = asyncio.create_task(download_picture(url, session, num))
            tasks.append(task)
        await asyncio.gather(*tasks)


def asyncio_download(urls):
    loop = asyncio.new_event_loop()
    loop.run_until_complete(download_all_pictures(urls))
    loop.close()


def sync_download(urls):
    with requests.Session() as session:
        for url, num in urls:
            with session.get(url) as response:
                content = response.content
                with open('artifacts/picture' + str(num) + '.png', 'wb') as f:
                    f.write(content)


if __name__ == "__main__":
    number = 20
    site = 'https://picsum.photos/'
    urls = [(site + str(randint(400, 1000)) + '/' + str(randint(400, 1000)), i + 1) for i in range(number)]
    start = time.time()
    asyncio_download(urls)  # 2s
    # sync_download(urls)  # 15s
    end = time.time()
    print(end - start)

