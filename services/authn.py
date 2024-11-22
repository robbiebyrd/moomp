import hashlib
import re

import bcrypt

from models.account import Account
from models.character import Character
from templates.utils.authn.authn import AuthNUtils
from utils.db import connect_db

connect_db()


class AuthNService:

    def __init__(self):
        self._config = AuthNUtils().config

    @staticmethod
    def authorize(email: str, password: str):
        if email and password:
            account = Account.objects(email=email).first()
            if account is not None:
                return (
                    account
                    if bcrypt.checkpw(
                        password.encode("utf-8"), account.password.encode("utf-8")
                    )
                    else None
                )

    @staticmethod
    def characters(account: Account):
        if account:
            return Character.objects(account=account).all()

    @staticmethod
    def password(username: str, new_password: str):
        if not username or not new_password:
            return False
        char = Character.objects(name=username).first()
        char.update(password=hashlib.sha256(new_password.encode("utf-8")).hexdigest())
        return True

    def email_policy(self, email: str):
        return email.split("@")[-1] not in self._config.disallowed_domains

    def password_policy(self, password: str, policy_group: str = "default"):
        policy_checks = [
            self._config.password_policies[policy]
            for policy in self._config.password_policy_groups.get(policy_group)
        ]

        return all(
            re.search(policy_check, password) is not None
            for policy_check in policy_checks
        )

    @staticmethod
    def encrypt_password(password: str):
        return bcrypt.hashpw(str.encode(password), bcrypt.gensalt()).decode("utf-8")
