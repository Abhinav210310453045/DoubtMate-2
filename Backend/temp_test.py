import asyncio
import aioboto3
import os
from dotenv import load_dotenv
load_dotenv()

from shared.src.utils.helper.DynamoDB import DynamoDB

REGION = os.environ.get('AWS_REGION', 'ap-south-1')
PROFILE = os.environ.get('AWS_PROFILE')

async def test_connection():
    db = DynamoDB(region=REGION, profile_name=PROFILE)
    try:
        await db.connect()
        print("✅ Connected to DynamoDB successfully!")

        # List tables
        session = aioboto3.Session(profile_name=PROFILE)
        async with session.client('dynamodb', region_name=REGION) as client:
            tables = await client.list_tables()
            print("📋 Available tables:", tables["TableNames"])

        # Use exact table name
        table_name = "users"
        table = db.get_table(table_name)
        response = await table.scan()
        items = response.get('Items', [])
        print(f"✅ Fetched {len(items)} items from '{table_name}'")

    except Exception as e:
        print("❌ Error connecting to DynamoDB:", str(e))

    finally:
        await db.disconnect()
        print("🔌 Disconnected from DynamoDB.")

if __name__ == "__main__":
    asyncio.run(test_connection())
