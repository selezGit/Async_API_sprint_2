import aioredis_cluster
import asyncio


async def wait_redis():
    client = await aioredis_cluster.create_redis_cluster(["redis://redis-node-0",
                              "redis://redis-node-1",
                              "redis://redis-node-2",
                              "redis://redis-node-3",
                              "redis://redis-node-4",
                              "redis://redis-node-5",
                              ])
    response = await client.ping()
    while not response:
        await asyncio.sleep(2)
        print("Redis-Cluster is unavailable - sleeping")
        response = await client.ping()
    #await client.close()
    print("Redis-Cluster is run")


if __name__ == '__main__':
    asyncio.run(wait_redis())

