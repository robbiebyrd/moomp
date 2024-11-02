from middleware import notify_and_create_event
from models.account import Account, AccountCreateDTO, AccountPasswordUpdateDTO
from services.authn import AuthNService
from utils.db import connect_db

connect_db()


class AccountService:

    @staticmethod
    def get_by_email_address(email: str) -> Account:
        return Account.objects(email=email).first()

    @staticmethod
    def register(acct: AccountCreateDTO):
        if Account.objects(email=acct.email).first():
            raise ValueError(f"An Account with email {acct.email} already exists.")
        if not AuthNService().email_policy(acct.email):
            raise ValueError(f"The domain for email {acct.email} is not allowed.")

        acct.password = AuthNService.encrypt_password(acct.password)
        acct_record = Account(**acct.model_dump(exclude_none=True)).save()

        notify_and_create_event("account", acct_record, "Created")

        return acct_record

    @classmethod
    def update(cls, acct: AccountCreateDTO):
        if fetched_account := cls.get_by_email_address(email=acct.email) is None:
            raise ValueError(f"An account with the email {acct.email} does not exist.")
        return fetched_account.update(**acct.model_dump(exclude_none=True)).save()

    @classmethod
    def change_password(cls, password_update: AccountPasswordUpdateDTO):
        # Check the password to ensure it meets all of our required safeguards.
        if AuthNService().password_policy(password_update.new_password) is False:
            raise ValueError("The new password did not meet the minimum policies.")
        if cls.get_by_email_address(password_update.email) is None:
            raise ValueError(
                f"The provided email address {password_update.email} was not found in our system."
            )
        if (
            authed_acct := AuthNService.authorize(
                password_update.email, password_update.current_password
            )
        ) is None:
            raise ValueError("The current password provided was invalid.")

        # Now that we have passed all the checks, change the password, save the record and return it.
        authed_acct.password = AuthNService.encrypt_password(
            password_update.new_password
        )
        return authed_acct.save()