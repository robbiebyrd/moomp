from mongoengine import signals

from middleware.updater import notify_modified, notify_deleted
from utils.types import OBJECT_TYPES

for object_type in OBJECT_TYPES:
    signals.post_save.connect(notify_modified, sender=object_type)
    signals.post_delete.connect(notify_deleted, sender=object_type)
