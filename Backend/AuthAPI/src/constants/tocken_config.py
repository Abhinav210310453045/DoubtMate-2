import os
from dotenv import load_dotenv

# Load variables from .env file if present
load_dotenv()

# -------------------------
# 🔐 JWT Token Config
# -------------------------

# Secret key for encoding and decoding JWT
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_default_dev_secret_key")

# Algorithm to use for JWT
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

# Access token expires in X minutes
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))

# Refresh token expires in X days
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
