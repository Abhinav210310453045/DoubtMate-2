from elasticsearch import AsyncElasticsearch
import asyncio

async def check_connection():
    es = AsyncElasticsearch(hosts=["http://localhost:9200"])
    info = await es.info()
    print(info)
    await es.close()
if __name__ == "__main__":
    asyncio.run(check_connection())
