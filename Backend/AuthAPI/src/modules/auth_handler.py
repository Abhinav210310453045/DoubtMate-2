from jose import JWTError, jwt
from datetime import datetime, timedelta,timezone
from typing import Optional, Dict
from AuthAPI.src.constants.tocken_config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS
)

class AuthHandler:
    def __init__(self):
        self.secret_key = SECRET_KEY
        self.algorithm = ALGORITHM
        self.access_token_expire_minutes = ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_days = REFRESH_TOKEN_EXPIRE_DAYS

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def create_refresh_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=self.refresh_token_expire_days)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode_token(self, token: str) -> Optional[Dict]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return None

    def is_token_expired(self, token: str) -> bool:
        payload = self.decode_token(token)
        if not payload or "exp" not in payload:
            return True
        expiry_time = datetime.fromtimestamp(payload["exp"], timezone.utc)
        return datetime.now(timezone.utc) > expiry_time
    def verify_token(self, token: str) -> Optional[Dict]:
        """
        Verifies the token by decoding and checking expiration.
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            # Check expiry
            exp = payload.get("exp")
            if exp is None or datetime.now(timezone.utc) > datetime.fromtimestamp(exp, timezone.utc):
                return None
            return payload
        except JWTError:
            return None