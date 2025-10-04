import jwt
from datetime import datetime, timedelta
from typing import Dict

class JWTService:
    def __init__(self, secret_key: str = "SECRET_KEY", algorithm: str = "HS256", expires_minutes: int = 60*24):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expires_minutes = expires_minutes

    def generate_token(self, data: Dict) -> str:
        """Gera token JWT"""
        payload = data.copy()
        payload.update({"exp": datetime.utcnow() + timedelta(minutes=self.expires_minutes)})
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> Dict:
        """Decodifica token JWT"""
        return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
