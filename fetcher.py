import aiohttp
import asyncio
from typing import List, Optional

async def fetch_url(session: aiohttp.ClientSession, url: str, timeout: int = 15) -> Optional[List[str]]:
    """Fetch rules from a single URL and return cleaned lines."""
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout)) as response:
            response.raise_for_status()
            content = await response.text(encoding="utf-8")
            # Split into lines, skip comments/empty lines
            rules = [
                line.strip() 
                for line in content.splitlines() 
                if line.strip() and not line.startswith(("!", "#"))
            ]
            return rules
    except Exception as e:
        print(f"⚠️ Error fetching {url}: {str(e)}")
        return None

async def fetch_all_rules(urls: List[str], concurrency: int) -> List[str]:
    """Fetch rules from multiple URLs in parallel."""
    connector = aiohttp.TCPConnector(limit=concurrency)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        # Flatten and filter out failed fetches
        all_rules = []
        for result in results:
            if result:
                all_rules.extend(result)
        return all_rules
