import aioboto3
from boto3.dynamodb.conditions import Key, Attr

class DynamoDB:
    """
    Singleton class for managing DynamoDB connections and operations using aioboto3.
    """
    _instance = None
    _session = None
    _dynamodb = None
    _region = 'eu-north-1'
    _profile_name = 'DoubtMate'

    @classmethod
    async def connect(cls, region='ap-south-1', profile_name=None):
        if cls._instance is None:
            cls._instance = cls
            cls._region = region
            cls._profile_name = profile_name
            cls._session = aioboto3.Session(profile_name=cls._profile_name)
            cls._dynamodb = await cls._session.resource('dynamodb', region_name=cls._region).__aenter__()
        return cls._instance

    @classmethod
    async def disconnect(cls):
        if cls._dynamodb:
            await cls._dynamodb.__aexit__(None, None, None)
            cls._dynamodb = None
            cls._session = None
            cls._instance = None

    @classmethod
    async def get_table(cls, table_name):
        if not cls._dynamodb:
            raise Exception("Call connect() before using this class!")
        return await cls._dynamodb.Table(table_name)

    # ----------- BASIC CRUD -----------
    @classmethod
    async def create_item(cls, table_name, item):
        table = await cls.get_table(table_name)
        response = await table.put_item(Item=item)
        return response

    @classmethod
    async def find_all(cls, table_name):
        table = await cls.get_table(table_name)
        response = await table.scan()
        return response.get('Items', [])

    @classmethod
    async def find_one(cls, table_name, key):
        table = await cls.get_table(table_name)
        response = await table.get_item(Key=key)
        return response.get('Item')
    @classmethod
    async def query_by_index(
        cls, table_name: str, index_name: str, key_name: str, key_value: str, limit: int = 1
    ):
        table = await cls.get_table(table_name)
        response = await table.query(
            IndexName=index_name,
            KeyConditionExpression=Key(key_name).eq(key_value),
            Limit=limit
        )
        items = response.get("Items", [])
        return items[0] if items else None


    @classmethod
    async def update_one(cls, table_name, key, update_expression, expression_values, expression_names=None):
        table = await cls.get_table(table_name)
        kwargs = {
            "Key": key,
            "UpdateExpression": update_expression,
            "ExpressionAttributeValues": expression_values,
            "ReturnValues": "ALL_NEW"
        }
        if expression_names:
            kwargs["ExpressionAttributeNames"] = expression_names
        response = await table.update_item(**kwargs)
        return response.get('Attributes')

    @classmethod
    async def delete_one(cls, table_name, key):
        table = await cls.get_table(table_name)
        response = await table.delete_item(Key=key)
        return response

    @classmethod
    async def delete_all(cls, table_name, key_name='id'):
        items = await cls.find_all(table_name)
        deleted = 0
        for item in items:
            await cls.delete_one(table_name, {key_name: item[key_name]})
            deleted += 1
        return f"Deleted {deleted} items"

    # ----------- EXTRA / OPTIONAL -----------
    @classmethod
    async def query(cls, table_name, key_condition_expression, expression_values, expression_names=None, index_name=None):
        table = await cls.get_table(table_name)
        kwargs = {
            "KeyConditionExpression": key_condition_expression,
            "ExpressionAttributeValues": expression_values
        }
        if expression_names:
            kwargs["ExpressionAttributeNames"] = expression_names
        if index_name:
            kwargs["IndexName"] = index_name
        response = await table.query(**kwargs)
        return response.get('Items', [])

    @classmethod
    async def batch_write(cls, table_name, put_items=None, delete_keys=None):
        table = await cls.get_table(table_name)
        async with table.batch_writer() as batch:
            if put_items:
                for item in put_items:
                    await batch.put_item(Item=item)
            if delete_keys:
                for key in delete_keys:
                    await batch.delete_item(Key=key)
        return {"put_count": len(put_items or []), "delete_count": len(delete_keys or [])}

    @classmethod
    async def batch_get(cls, table_name, keys):
        table = await cls.get_table(table_name)
        response = await table.batch_get_item(
            RequestItems={table_name: {"Keys": keys}}
        )
        return response["Responses"].get(table_name, [])

    @classmethod
    async def filtered_scan(cls, table_name, filter_expression, expression_values, expression_names=None):
        table = await cls.get_table(table_name)
        kwargs = {
            "FilterExpression": filter_expression,
            "ExpressionAttributeValues": expression_values
        }
        if expression_names:
            kwargs["ExpressionAttributeNames"] = expression_names
        response = await table.scan(**kwargs)
        return response.get('Items', [])

    @classmethod
    async def count(cls, table_name):
        table = await cls.get_table(table_name)
        response = await table.scan(Select='COUNT')
        return response.get('Count', 0)

    @classmethod
    async def exists(cls, table_name, key):
        item = await cls.find_one(table_name, key)
        return item is not None

    @classmethod
    async def increment_field(cls, table_name, key, field, delta=1):
        table = await cls.get_table(table_name)
        response = await table.update_item(
            Key=key,
            UpdateExpression=f"ADD {field} :inc",
            ExpressionAttributeValues={":inc": delta},
            ReturnValues="UPDATED_NEW"
        )
        return response.get("Attributes", {})

