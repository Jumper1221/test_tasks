import asyncio
import json

import aiohttp
from aiohttp import ClientTimeout

urls = [
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
]


async def fetch_one_url(
    url: str, session: aiohttp.ClientSession, semaphore: asyncio.Semaphore
):
    try:
        async with semaphore:
            async with session.get(url) as response:
                await response.read()
                return (url, response.status)
    except Exception:
        return (url, 0)


async def fetch_urls(urls: list[str], file_path: str):
    semaphore = asyncio.Semaphore(5)
    timeout = ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [fetch_one_url(url, session, semaphore) for url in urls]
        results = await asyncio.gather(*tasks)
    results_dct = {url: status for url, status in results}

    with open(file_path, "w") as f:
        for url in urls:
            status = results_dct.get(url, 0)
            json_line = json.dumps({"url": url, "status_code": status})
            f.write(json_line + "\n")

    return results_dct


if __name__ == "__main__":
    asyncio.run(fetch_urls(urls, "./results.jsonl"))
