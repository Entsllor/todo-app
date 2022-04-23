from passlib.context import CryptContext
from src.core.settings import get_settings

pwd_context = CryptContext(schemes=get_settings().PASSWORD_HASHING_SCHEMAS)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)
