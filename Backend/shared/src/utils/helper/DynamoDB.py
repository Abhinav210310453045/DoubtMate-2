import aioboto3
from boto3.dynamodb.conditions import Key, Attr

class DynamoDB:
    def __init__(self, region='ap-south-1', profile_name=None):
        self.region = region
        self.profile_name = profile_name
        self._session = None
        self._dynamodb = None

    async def connect(self):
        self._session = aioboto3.Session(profile_name=self.profile_name)
        self._dynamodb = await self._session.resource('dynamodb', region_name=self.region).__aenter__()

    async def disconnect(self):
        if self._dynamodb:
            await self._dynamodb.__aexit__(None, None, None)

    async def get_table(self, table_name):
        if not self._dynamodb:
            raise Exception("Call connect() before using this class!")
        return await self._dynamodb.Table(table_name)
    # ----------- BASIC CRUD -----------

    async def create_item(self, table_name, item):
        table = self.get_table(table_name)
        response = await table.put_item(Item=item)
        return response

    async def find_all(self, table_name):
        table = self.get_table(table_name)
        response = await table.scan()
        return response.get('Items', [])

    async def find_one(self, table_name, key):
        table = self.get_table(table_name)
        response = await table.get_item(Key=key)
        return response.get('Item')

    async def update_one(self, table_name, key, update_expression, expression_values, expression_names=None):
        table = self.get_table(table_name)
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

    async def delete_one(self, table_name, key):
        table = self.get_table(table_name)
        response = await table.delete_item(Key=key)
        return response

    async def delete_all(self, table_name, key_name='id'):
        items = await self.find_all(table_name)
        deleted = 0
        for item in items:
            await self.delete_one(table_name, {key_name: item[key_name]})
            deleted += 1
        return f"Deleted {deleted} items"

    # ----------- EXTRA / OPTIONAL -----------

    # Query by partition key (optionally by sort key)
    async def query(self, table_name, key_condition_expression, expression_values, expression_names=None, index_name=None):
        table = self.get_table(table_name)
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

    # Batch write (put/delete multiple items)
    async def batch_write(self, table_name, put_items=None, delete_keys=None):
        table = self.get_table(table_name)
        async with table.batch_writer() as batch:
            if put_items:
                for item in put_items:
                    await batch.put_item(Item=item)
            if delete_keys:
                for key in delete_keys:
                    await batch.delete_item(Key=key)
        return {"put_count": len(put_items or []), "delete_count": len(delete_keys or [])}

    # Batch get (fetch multiple items by keys)
    async def batch_get(self, table_name, keys):
        table = self.get_table(table_name)
        response = await table.batch_get_item(
            RequestItems={table_name: {"Keys": keys}}
        )
        return response["Responses"].get(table_name, [])

    # Scan with filter expression
    async def filtered_scan(self, table_name, filter_expression, expression_values, expression_names=None):
        table = self.get_table(table_name)
        kwargs = {
            "FilterExpression": filter_expression,
            "ExpressionAttributeValues": expression_values
        }
        if expression_names:
            kwargs["ExpressionAttributeNames"] = expression_names
        response = await table.scan(**kwargs)
        return response.get('Items', [])

    # Count (number of items in the table)
    async def count(self, table_name):
        table = self.get_table(table_name)
        response = await table.scan(Select='COUNT')
        return response.get('Count', 0)

    # Exists (returns True if the item exists, else False)
    async def exists(self, table_name, key):
        item = await self.find_one(table_name, key)
        return item is not None

    # Atomic increment/decrement a numeric field
    async def increment_field(self, table_name, key, field, delta=1):
        table = self.get_table(table_name)
        response = await table.update_item(
            Key=key,
            UpdateExpression=f"ADD {field} :inc",
            ExpressionAttributeValues={":inc": delta},
            ReturnValues="UPDATED_NEW"
        )
        return response.get("Attributes", {})

