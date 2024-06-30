import hashlib

import bcrypt

from models.account import Account
from models.character import Character
from utils.db import connect_db


class AuthNService:

    def __init__(self):
        self._connection = connect_db()

    @classmethod
    def authorize(cls, email: str, password: str):
        if email and password:
            account = Account.objects(email=email).first()
            if account is not None:
                return account if bcrypt.checkpw(password.encode("utf-8"), account.password.encode("utf-8")) else None

    @classmethod
    def characters(cls, account: Account):
        if account:
            return Character.objects(account=account).all()

    @classmethod
    def password(cls, username: str, new_password: str):
        if not username or not new_password:
            return False
        char = Character.objects(name=username).first()
        char.update(password=hashlib.sha256(new_password.encode("utf-8")).hexdigest())
        return True

    @staticmethod
    def encrypt_password(password: str):
        return bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
