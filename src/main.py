import asyncio
import os.path

import aiohttp
import nftrade
import pancakeswap

from pysondb import db

from logger_utility import create_logger

job_params = [*nftrade.job_params, *pancakeswap.job_params]

logger = create_logger(__name__, os.path.realpath("ntf.log"))


async def main():
    while True:
        async with aiohttp.ClientSession() as session:
            data_entries = await asyncio.gather(*[param["func"](session, param) for param in job_params])
            data_entries = [entry for entry in data_entries if entry]
            nft_db = db.getDb(os.path.realpath("db.json"))
            nft_db.addMany(data_entries)
            logger.info(
                f"job number {len(job_params)}, success job number {len(data_entries)}, failed job number {len(job_params) - len(data_entries)}")
        interval = 10
        logger.info(f"sleep {interval} seconds")
        await asyncio.sleep(interval)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

