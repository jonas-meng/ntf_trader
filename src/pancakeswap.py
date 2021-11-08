import time


async def track_lowest_price(session, params):
    payload = {
        "query": "\n        query getNftsMarketData($first: Int, $skip: Int!, $where: NFT_filter, $orderBy: NFT_orderBy, $orderDirection: OrderDirection) {\n          nfts(where: $where, first: $first, orderBy: $orderBy, orderDirection: $orderDirection, skip: $skip) {\n            \n  tokenId\n  metadataUrl\n  currentAskPrice\n  currentSeller\n  latestTradedPriceInBNB\n  tradeVolumeBNB\n  totalTrades\n  isTradable\n  updatedAt\n  otherId\n  collection {\n    id\n  }\n\n            transactionHistory {\n              \n  id\n  block\n  timestamp\n  askPrice\n  netPrice\n  withBNB\n  buyer {\n    id\n  }\n  seller {\n    id\n  }\n\n            }\n          }\n        }\n      ",
        "variables": {
            "where": {
                "collection": params["collection"],
                "isTradable": True
            },
            "first": 1,
            "skip": 0,
            "orderBy": "currentAskPrice",
            "orderDirection": "asc"
        }
    }
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json",
        "Origin": "https://pancakeswap.finance",
        "Referer": "https://pancakeswap.finance",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
    }
    async with session.post(params["url"], json=payload, headers=headers) as response:
        try:
            if response.status == 200:
                nft_data = await response.json()
                return {
                    "exchange": "pancakeswap",
                    "timestamp": int(time.time()),
                    "data": nft_data["data"]["nfts"][0]
                }
            else:
                return None
        except Exception:
            return None


job_params = [
    {
        "url": "https://api.thegraph.com/subgraphs/name/pancakeswap/nft-market",
        "func": track_lowest_price,
        "collection": "0x0a8901b0e25deb55a87524f0cc164e9644020eba"
    }, {
        "url": "https://api.thegraph.com/subgraphs/name/pancakeswap/nft-market",
        "func": track_lowest_price,
        "collection": "0xdf7952b35f24acf7fc0487d01c8d5690a60dba07"
    }, {
        "url": "https://api.thegraph.com/subgraphs/name/pancakeswap/nft-market",
        "func": track_lowest_price,
        "collection": "0x3da8410e6ef658c06e277a2769816688c37496cf"
    }
]
