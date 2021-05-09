import aioredis_cluster
import asyncio
import repackage

repackage.up()

from settings import TestSettings 

SETTINGS = TestSettings()

async def wait_redis():
    client = await aioredis_cluster.create_redis_cluster(SETTINGS.redis_host)
    response = await client.ping()
    while not response:
        await asyncio.sleep(2)
        print("Redis-Cluster is unavailable - sleeping")
        response = await client.ping()
    print("Redis-Cluster is run")


if __name__ == '__main__':
    asyncio.run(wait_redis())

