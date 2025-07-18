# Doubt Mate

Doubt Mate is an AI-powered, fully personalized learning app for students. It enables students to learn, study, and evaluate their performance without hesitation, helping them improve their skills and address weaker study areas using advanced AI features. Key features include:

- Personalized tests and quizzes
- Doubt sessions
- Proctored exams
- Board exam-style tests
- Insights into personalized improvement areas

The platform is strictly aligned with the NCERT curriculum and leverages AI to provide a tailored learning experience. Doubt Mate also helps students learn effective exam strategies, inspired by top performers in recent board exams.

**Tech Stack:**
- Gemini API
- Vector Embeddings
- DynamoDB
- AWS
- Knowledge Graphs
- FastAPI
- JavaScript
- Python

---

# AsyncDynamoDBCRUD

A robust, easy-to-use **asynchronous DynamoDB CRUD helper class** for Python, built on [`aioboto3`](https://github.com/terrycain/aioboto3).

Supports standard CRUD, queries, batch operations, filtered scans, counters, and more—all with a reusable connection lifecycle.

---

## Features

- **Async/await everywhere** (great for FastAPI, Starlette, etc)
- No table name in constructor — specify it per operation
- **Connect once, reuse everywhere:** Efficient and scalable
- **Optional helpers:** query, batch ops, filtered scan, counter, existence check, and more
- Clean, extendable design

---

## Installation

```bash
pip install aioboto3 boto3
```

---

## Usage

### 1. Import & Initialize

```python
from your_module import AsyncDynamoDBCRUD  # Replace with your actual module name

db = AsyncDynamoDBCRUD(region='ap-south-1')
```

### 2. Connect Once at App Startup

```python
await db.connect()
```

### 3. CRUD Operations

#### Create

```python
await db.create_item('Users', {'id': '1', 'name': 'Abhinav'})
```

#### Read (Get One)

```python
item = await db.find_one('Users', {'id': '1'})
```

#### Read All

```python
users = await db.find_all('Users')
```

#### Update

```python
# Example: Update name
await db.update_one(
    'Users',
    {'id': '1'},
    'SET #nm = :n',
    {':n': 'New Name'},
    {'#nm': 'name'}
)
```

#### Delete One

```python
await db.delete_one('Users', {'id': '1'})
```

#### Delete All (CAUTION: Scans and deletes each item!)

```python
await db.delete_all('Users')
```

---

### 4. Advanced Methods

#### Query by Partition/Sort Key

```python
from boto3.dynamodb.conditions import Key

results = await db.query(
    'Orders',
    key_condition_expression=Key('user_id').eq('123'),
    expression_values={':val': '123'}
)
```

#### Batch Write

```python
await db.batch_write('Users', put_items=[{'id': '2', 'name': 'Alice'}])
```

#### Batch Get

```python
users = await db.batch_get('Users', keys=[{'id': '1'}, {'id': '2'}])
```

#### Filtered Scan

```python
from boto3.dynamodb.conditions import Attr

results = await db.filtered_scan(
    'Users',
    filter_expression=Attr('active').eq(True),
    expression_values={}
)
```

#### Count Items

```python
total = await db.count('Users')
```

#### Exists Check

```python
exists = await db.exists('Users', {'id': '1'})
```

#### Atomic Increment/Decrement

```python
await db.increment_field('Users', {'id': '1'}, 'login_count', 1)
```

---

### 5. Disconnect at App Shutdown

```python
await db.disconnect()
```

---

## Best Practices

- **Connection:**  
  Call `connect()` once at startup, and `disconnect()` once at shutdown—**not per request**.
- **Error Handling:**  
  Consider wrapping CRUD calls in try/except in production.
- **Indexes:**  
  For `query` and `filtered_scan`, use the right indexes for performance.
- **Table Schema:**  
  Pass the correct key(s) and attribute names as per your DynamoDB schema.

---

## Example: FastAPI Integration

```python
# In your FastAPI app
from fastapi import FastAPI

app = FastAPI()
db = AsyncDynamoDBCRUD(region='ap-south-1')

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
```

---

## License

This project is open source and licensed under the MIT License.

---
