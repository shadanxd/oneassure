import jwt
from fastapi import HTTPException
from fastapi.security import HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv


class AuthHandler:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes = ['bcrypt'], deprecated='auto')
    load_dotenv()
    secret = os.getenv('secret')
    timeout = os.getenv('token_timeout')

    @classmethod
    def get_password_hash(cls, password: str):
        return cls.pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def encode_token(cls, username):
        payload = {'exp': datetime.utcnow() + timedelta(days = 0, minutes = int(cls.timeout)),
                   'iat': datetime.utcnow(), 'sub': username}

        return jwt.encode(payload, cls.secret, algorithm='HS256')

    @classmethod
    def decode_token(cls, token):
        try:
            payload = jwt.decode(token, cls.secret, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code = 401, detail = 'Signature has expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code = 401, detail = 'Invalid token')
