import uuid
from datetime import datetime, timezone

from AuthAPI.src.models.schemas import UserRegister, UserLogin, UserInDB
from AuthAPI.src.modules.auth_handler import AuthHandler
from AuthAPI.src.modules.password_hasher import PasswordHasher
from shared.src.utils.helper.DynamoDB import DynamoDB  # This uses the connected instance


class UserService:
    def __init__(self, table_name: str = "Users"):
        self.table_name = table_name
        self.auth_handler = AuthHandler()
        self.password_hasher = PasswordHasher()

    async def register_user(self, user: UserRegister):
        existing_user = await DynamoDB.find_one(self.table_name, {"username": user.username})
        if existing_user:
            return {"error": "User already exists"}, 409

        user_id = str(uuid.uuid4())
        hashed_pw = self.password_hasher.hash_password(user.password)
        now = datetime.now(timezone.utc).isoformat()

        user_item = {
            "user_id": user_id,
            "username": user.username,
            "email": user.email,
            "password_hash": hashed_pw,
            "role": user.role, 
            "created_at": now,
            "last_login": None
        }

        await DynamoDB.create_item(self.table_name, user_item)

        return {
            "message": "User registered successfully",
            "user_id": user_id
        }

    async def authenticate_user(self, credentials: UserLogin):
        user_data = await DynamoDB.find_one(self.table_name, {"username": credentials.username})
        if not user_data:
            return {"error": "Invalid username or password"}, 401

        valid = self.password_hasher.verify_password(
            credentials.password,
            user_data.get("password_hash")
        )

        if not valid:
            return {"error": "Invalid username or password"}, 401

        await DynamoDB.update_one(
            self.table_name,
            {"username": credentials.username},
            "SET last_login = :t",
            expression_values={":t": datetime.now(timezone.utc).isoformat()}
        )

        payload = {
            "sub": user_data["username"],
            "user_id": user_data["user_id"],
            "role": user_data["role"]
        }

        access_token = self.auth_handler.create_access_token(payload)
        refresh_token = self.auth_handler.create_refresh_token(payload)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    async def get_user_by_username(self, username: str) -> UserInDB | None:
        user_data = await DynamoDB.find_one(self.table_name, {"username": username})
        if not user_data:
            return None

        return UserInDB(**user_data)
