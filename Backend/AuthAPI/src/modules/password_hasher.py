import bcrypt


class PasswordHasher:
    def __init__(self, rounds: int = 12):
        self.rounds = rounds  # 12 is secure enough for production

    def hash_password(self, password: str) -> str:
        """
        Hash a plaintext password using bcrypt.
        Returns the hashed password as a UTF-8 string.
        """
        salt = bcrypt.gensalt(rounds=self.rounds)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plaintext password against the stored bcrypt hash.
        Returns True if they match, else False.
        """
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
