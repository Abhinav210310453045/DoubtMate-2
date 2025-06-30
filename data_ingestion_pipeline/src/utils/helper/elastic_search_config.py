from elasticsearch import AsyncElasticsearch, helpers, exceptions

class ElasticCRUDAsync:
    def __init__(self, host: str = "http://localhost:9200"):
        self.client = AsyncElasticsearch(hosts=[host])

    # ---------------------- INDEX ----------------------
    async def create_index(self, index: str, mappings: dict = None):
        exists = await self.client.indices.exists(index=index)
        if not exists:
            await self.client.indices.create(index=index, body=mappings or {})
            print(f"Index '{index}' created.")

    async def delete_index(self, index: str):
        exists = await self.client.indices.exists(index=index)
        if exists:
            await self.client.indices.delete(index=index)
            print(f"Index '{index}' deleted.")

    # ---------------------- INSERT ----------------------
    async def insert_one(self, index: str, doc_id: str, doc: dict):
        return await self.client.index(index=index, id=doc_id, document=doc)

    async def insert_many(self, index: str, docs: list[dict]):
        actions = [{"_index": index, "_source": doc} for doc in docs]
        return await helpers.async_bulk(self.client, actions)

    # ---------------------- READ ----------------------
    async def get_one(self, index: str, doc_id: str):
        try:
            result = await self.client.get(index=index, id=doc_id)
            return result["_source"]
        except exceptions.NotFoundError:
            return None

    async def get_all(self, index: str):
        query = {"query": {"match_all": {}}}
        return await self._scroll_search(index, query)

    async def search(self, index: str, query_dict: dict):
        query = {"query": query_dict}
        return await self._scroll_search(index, query)

    async def search_by_field(self, index: str, field: str, value: str):
        return await self.search(index, {"match": {field: value}})

    # ---------------------- UPDATE ----------------------
    async def update_one(self, index: str, doc_id: str, fields: dict):
        return await self.client.update(index=index, id=doc_id, doc={"doc": fields})

    async def update_many(self, index: str, query_dict: dict, fields: dict):
        script = "; ".join([f"ctx._source.{k} = '{v}'" for k, v in fields.items()])
        query = {
            "script": {"source": script},
            "query": query_dict
        }
        return await self.client.update_by_query(index=index, body=query)

    # ---------------------- DELETE ----------------------
    async def delete_one(self, index: str, doc_id: str):
        try:
            return await self.client.delete(index=index, id=doc_id)
        except exceptions.NotFoundError:
            return {"result": "not_found"}

    async def delete_many(self, index: str, query_dict: dict):
        return await self.client.delete_by_query(index=index, body={"query": query_dict})

    # ---------------------- VECTOR SEARCH (Optional) ----------------------
    async def knn_search(self, index: str, vector: list[float], k: int = 5):
        query = {
            "knn": {
                "embedding": {
                    "vector": vector,
                    "k": k
                }
            }
        }
        return await self.client.search(index=index, body=query)

    # ---------------------- INTERNAL SCROLL SEARCH ----------------------
    async def _scroll_search(self, index: str, query: dict, scroll: str = "2m", size: int = 1000):
        results = []
        async for hit in helpers.async_scan(self.client, index=index, query=query, scroll=scroll, size=size):
            results.append(hit["_source"])
        return results

    # ---------------------- CLEANUP ----------------------
    async def close(self):
        await self.client.close()
