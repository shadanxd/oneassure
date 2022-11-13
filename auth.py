import jwt
import os
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
secret = os.environ.get('secret')


class AuthHandler:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes = ['bcrypt'], deprecated='auto')

    @classmethod
    def get_password_hash(cls, password: str):
        return cls.pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def encode_token(cls, username):
        payload = {'exp': datetime.utcnow() + timedelta(days = 0, minutes = 5),
                   'iat': datetime.utcnow(), 'sub': username}

        return jwt.encode(payload, secret, algorithm='HS256')

    @classmethod
    def decode_token(cls, token):
        try:
            payload = jwt.decode(token, secret, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code = 401, detail = 'Signature has expired')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code = 401, detail = 'Invalid token')
