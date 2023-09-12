import hashlib
import os

SALT = os.environ['SALT_KEY']

def get_password_hash(password: str) -> str:
    p = SALT + password
    hashed = hashlib.md5(p.encode())
    return hashed.hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    hashed = get_password_hash(plain_password)
    return hashed == hashed_password