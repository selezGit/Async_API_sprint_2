from elasticsearch import AsyncElasticsearch
import asyncio


async def wait_es():
    client = AsyncElasticsearch(hosts=["http://elasticsearch:9200", ])
    response = await client.ping()
    while not response:
        await asyncio.sleep(2)
        print('Elastic is unavailable - sleeping')
        response = await client.ping()
    await client.close()
    print("Elastic is run!")


if __name__ == '__main__':
    asyncio.run(wait_es())
