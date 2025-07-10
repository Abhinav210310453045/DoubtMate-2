from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
from shared.src.utils.helper.DynamoDB import DynamoDB
from AuthAPI.src.api.login import router as auth_router


load_dotenv()  
REGION = os.environ.get('AWS_REGION', 'eu-north-1')  # Default to 'ap-south-1' if not set
PROFILE = os.environ.get('AWS_PROFILE')  # Change as per your setup
print(f"Using AWS Region: {REGION}, Profile: {PROFILE}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: connect to DynamoDB (yielded for the app's lifetime)
    await DynamoDB.connect(region=REGION, profile_name=PROFILE)

    yield  # Application runs here

    # Shutdown: close DynamoDB connection
    await DynamoDB.disconnect()

app = FastAPI(lifespan=lifespan)

# Custom OpenAPI schema with JWT Bearer security
from fastapi.security import HTTPBearer

def custom_openapi():
    app.openapi_schema = None  # force refresh on each reload

    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="DoubtMate API",
        version="1.0.0",
        description="API with JWT authentication for DoubtMate",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    # Secure all endpoints except /auth/login and /auth/register
    for path in openapi_schema["paths"]:
        if not (path.startswith("/auth/login") or path.startswith("/auth/register")):
            for method in openapi_schema["paths"][path]:
                openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Add CORS (open to all for development; restrict in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Example: Add authentication router with proper tagging
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to DoubtMate!"}



# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)