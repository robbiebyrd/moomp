from pydantic import BaseModel


class ConfigAuthN(BaseModel, extra='allow'):
    password_policies: dict[str, str]
    password_policy_groups: dict[str, list[str]]
    disallowed_domains: list[str]
