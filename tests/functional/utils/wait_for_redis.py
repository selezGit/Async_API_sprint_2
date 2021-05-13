import aioredis
import asyncio
import repackage

repackage.up()

from settings import SETTINGS, logger

async def wait_redis():
    client = await aioredis.create_redis_pool((SETTINGS.redis_host, SETTINGS.redis_port), minsize=10, maxsize=20)
    response = await client.ping()
    while not response:
        await asyncio.sleep(2)
        logger.info("Redis-Cluster is unavailable - sleeping")
        response = await client.ping()
    logger.info("Redis-Cluster is run")


if __name__ == '__main__':
    asyncio.run(wait_redis())

