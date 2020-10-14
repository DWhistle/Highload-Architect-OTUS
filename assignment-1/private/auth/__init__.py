import hashlib
import os
from private.db.repo.user_repo import UserRepo


def generate_salt():
    return os.urandom(10).hex()


def encode_password(password, salt):
    return hashlib.md5(bytes(password, encoding='utf-8')).hexdigest() + salt


def authenticate(username, password):
    user = UserRepo.get_user_creds_by_username(username)
    if user and user.user_pass == encode_password(password, user.password_salt):
        return user
