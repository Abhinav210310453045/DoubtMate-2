from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from shared.src.utils.helper.DynamoDB import DynamoDB  # Replace 'your_module' with the actual filename (without .py)
from contextlib import asynccontextmanager


REGION = os.environ.get('AWS_REGION', 'ap-south-1')  # Default to 'ap-south-1' if not set
PROFILE = os.environ.get('AWS_PROFILE')  # Change as per your setup

load_dotenv()  


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: connect to DynamoDB (yielded for the app's lifetime)
    app.state.db = DynamoDB(region=REGION, profile_name=PROFILE)
    await app.state.db.connect()

    yield  # Application runs here

    # Shutdown: close DynamoDB connection
    await app.state.db.disconnect()

app = FastAPI(lifespan=lifespan)
# Add CORS (open to all for development; restrict in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to Doubtmate!"}

# Example: How to get the db instance (for when you add endpoints)
def get_db():
    return app.state.db

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)