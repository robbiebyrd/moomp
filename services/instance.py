from models.instance import Instance
from utils.db import connect_db


class InstanceService:

    def __init__(self, instance_id: str):
        self._connection = connect_db()

        self._instance = Instance.objects(id=instance_id).first()

    def get_properties(self, prop: str | None = None):
        if prop is not None and hasattr(self._instance.properties, prop):
            return self._instance.properties[prop]
        return self._instance.properties
