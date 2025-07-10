import asyncio
import aioboto3
import os
from dotenv import load_dotenv
load_dotenv()

from shared.src.utils.helper.DynamoDB import DynamoDB

REGION = os.environ.get('AWS_REGION')
PROFILE = os.environ.get('AWS_PROFILE')
print(REGION, PROFILE)

async def test_dynamodb_singleton():
    try:
        # Connect using the singleton classmethod
        await DynamoDB.connect(region=REGION, profile_name=PROFILE)
        print("✅ Connected to DynamoDB successfully!")

        # List tables using aioboto3 directly for verification
        session = aioboto3.Session(profile_name=PROFILE)
        async with session.client('dynamodb', region_name=REGION) as client:
            tables = await client.list_tables()
            print("📋 Available tables:", tables["TableNames"])

        # Add one data item to a table (replace 'users' and item as needed)
        table_name = "users"
        item = {"username": "test_id_2", "name": "Test User", "email": "test1@example.com",'role':'student'}
        response = await DynamoDB.create_item(table_name, item)
        print(f"📝 Item insert response: {response}")

        # Disconnect
        await DynamoDB.disconnect()
        print("🔌 Disconnected from DynamoDB.")

    except Exception as e:
        print("❌ Error during DynamoDB operations:", str(e))

if __name__ == "__main__":
    asyncio.run(test_dynamodb_singleton())
