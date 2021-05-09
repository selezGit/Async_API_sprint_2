from elasticsearch import AsyncElasticsearch
import asyncio
import repackage

repackage.up()

from settings import TestSettings 

SETTINGS = TestSettings()


async def wait_es():
    client = AsyncElasticsearch(hosts=[SETTINGS.es_host, ])
    response = await client.ping()
    while not response:
        await asyncio.sleep(2)
        print('Elastic is unavailable - sleeping')
        response = await client.ping()
    await client.close()
    print("Elastic is run!")


if __name__ == '__main__':
    asyncio.run(wait_es())
