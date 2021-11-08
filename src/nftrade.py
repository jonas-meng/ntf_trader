import json
import time


async def track_lowest_price(session, params):
    async with session.get(params["url"]) as response:
        try:
            if response.status == 200:
                nft_data = await response.json()
                return {
                    "exchange": "nftrade",
                    "timestamp": int(time.time()),
                    "data": nft_data[0]
                }
            else:
                return None
        except Exception:
            return None


job_params = [
    {
        "url": "https://api.nftrade.com/api/v1/tokens?limit=1&skip=0&contracts[]=8089fc0b-1e44-4438-a72e-1b70895298c5&chains[]=56&search=&sort=price_asc",
        "func": track_lowest_price
    }
]
