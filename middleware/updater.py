import paho.mqtt.publish as publish


def notify_modified(sender, document, created):
    notify(sender.__name__, document, "Created" if created else "Updated")


def notify_deleted(sender, document):
    notify(sender.__name__, document, "Deleted")


def notify(document_type, document, document_operation):
    publish.single(f"/{document_type}/{document.id}/{document_operation}", document.to_json(), hostname="localhost")
