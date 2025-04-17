import asyncio
import json

import aiofiles
import aiohttp
from aiohttp import ClientTimeout


async def fetch_urls(urls_file: str, output_file: str):
    async with aiofiles.open(urls_file, "r") as fl:
        urls = [line.strip() async for line in fl]

    queue = asyncio.Queue()

    writer_task = asyncio.create_task(write_results(output_file, queue))

    semaphore = asyncio.Semaphore(5)
    async with aiohttp.ClientSession() as session:
        tasks = [process_url(url, session, semaphore, queue) for url in urls]
        await asyncio.gather(*tasks)

    await queue.put(None)
    await writer_task


async def process_url(url, session, semaphore, queue):
    async with semaphore:
        try:
            async with session.get(url, timeout=ClientTimeout(total=30)) as response:
                if response.status == 200:
                    try:
                        content = await response.json()
                        await queue.put({"url": url, "content": content})
                    except json.JSONDecodeError:
                        print(f"Invalid JSON response from {url}")
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")


async def write_results(output_file, queue):
    async with aiofiles.open(output_file, "w") as fl:
        while True:
            item = await queue.get()
            if item is None:
                break
            line = json.dumps({"url": item["url"], "content": item["content"]}) + "\n"
            await fl.write(line)


if __name__ == "__main__":
    asyncio.run(fetch_urls("urls.txt", "./results_hard.jsonl"))
