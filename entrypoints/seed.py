import json
from typing import Type

from mongoengine import Document
from pydantic import BaseModel

from models.account import Account
from models.character import Character
from models.instance import Instance
from models.object import Object
from models.portal import Portal
from models.room import Room
from models.script import Script
from services.authn import AuthNService


class ModelSettings(BaseModel):
    item_type: Type[Document]
    named_field: str
    search_fields: dict
    hydrate_fields: list[tuple[str, str]]


class Seeder:

    def __init__(self, file: str = None):
        if file is None:
            raise ValueError("A JSON file is required to seed the database.")
        with open(file, "r") as f:
            self._content = json.load(f)

        self.model_type_settings = {
            "instance": ModelSettings(
                item_type=Instance,
                named_field="name",
                search_fields={"name": "name"},
                hydrate_fields=[("instance", "parent")],
            ),
            "account": ModelSettings(
                item_type=Account,
                named_field="email",
                search_fields={"email": "email"},
                hydrate_fields=[("instance", "instance")],
            ),
            "character": ModelSettings(
                item_type=Character,
                named_field="name",
                search_fields={"name": "name"},
                hydrate_fields=[("account", "account")],
            ),
            "room": ModelSettings(
                item_type=Room,
                named_field="name",
                search_fields={"name": "name"},
                hydrate_fields=[("character", "character"), ("room", "parent")],
            ),
            "portal": ModelSettings(
                item_type=Portal,
                named_field="name",
                search_fields={
                    "name": "name",
                    "from_room": "from_room",
                    "to_room": "to_room",
                },
                hydrate_fields=[
                    ("room", "to_room"),
                    ("room", "from_room"),
                    ("character", "owner"),
                ],
            ),
            "object": ModelSettings(
                item_type=Object,
                named_field="name",
                search_fields={"name": "name"},
                hydrate_fields=[
                    ("object", "parent"),
                    ("character", "owner"),
                    ("character", "holder"),
                    ("room", "room"),
                ],
            ),
        }

    def seed(self):
        # Encode passwords in accounts!
        if self._content.get("accounts"):
            for i, account in enumerate(self._content.get("accounts")):
                self._content.get("accounts")[i].update(
                    {"password": AuthNService.encrypt_password(account.get("password"))}
                )

        for model_type, model_settings in self.model_type_settings.items():
            for item in self._content.get(f"{model_type}s", []):
                self.seed_item(
                    item,
                    model_type,
                    model_settings.search_fields,
                    model_settings.hydrate_fields,
                )
        instance = Instance.objects.all()[0]
        characters = Character.objects()

        a = Script.objects.create(
            name="Test Script",
            instance=instance,
            scripts=[
                {
                    "script": """function(obj, obj1, obj2)
    mytable = {}
    mytable["msg"] = tostring(obj.name) .. " Test"
    mytable2 = {}
    mytable2["msg"] = tostring(obj2.name) .. "Test"
    d = "/Room/" .. tostring(obj["id"]) .. "/Properties/Update"
    return{ {d, mytable} }
end
""",
                    "topics": ["/Room/#", "/Character/#"],
                },
            ],
            owner=characters[0],
        )
        a.save()

    def hydrate(self, obj, model_type, field):
        if (
            self.model_type_settings[model_type] is not None
            and obj.get(field)
            and isinstance(obj[field], str)
        ):
            query = {self.model_type_settings[model_type].named_field: obj.get(field)}
            obj[field] = (
                self.model_type_settings[model_type].item_type.objects(**query).first()
            )
        return obj

    def seed_item(
        self,
        item,
        model_type,
        search_fields: dict,
        hydrate_fields: list[tuple[str, str]],
    ):
        if not self.model_type_settings[model_type].item_type:
            raise ValueError(f"Could not find model type {model_type}")

        print(f"Seeding {model_type}.")

        for hydrate in hydrate_fields:
            print(f"Hydrating field {hydrate[1]} of type {hydrate[0]}.")
            item = self.hydrate(item, *hydrate)
            print(f"Saving field {hydrate[1]} of type {hydrate[0]}.")

        updated_search_fields = {
            k[0]: item.get(k[1]) for k in list(search_fields.items())
        }

        if (
            existing_item := self.model_type_settings[model_type]
            .item_type.objects(**updated_search_fields)
            .first()
        ):
            print(f"Updating {model_type}: {updated_search_fields}.")
            # self.model_type_settings[model_type].item_type.modify(
            #     query=updated_search_fields, **item
            # )

        else:
            print(f"Creating {model_type}: {updated_search_fields}.")
            self.model_type_settings[model_type].item_type(**item).save()
            print(f"Saved item: {updated_search_fields}.")
