import json
import os

import paho.mqtt.publish as publish

from models.events import Event


def notify_modified(document_type, document, created):
    notify(document_type.__name__, document, "Created" if created else "Updated")


def notify_deleted(document_type, document):
    notify(document_type.__name__, document, "Deleted")


def notify_and_create_event(document_type, document, document_operation, operator=None):
    create_event(document, document_operation, operator)
    notify(document_type, document, document_operation, operator)


def notify(document_type, document, document_operation, operator=None):
    doc = json.loads(document.to_json(use_db_field=False))

    all_filtered_fields = ["_id"]

    filtered_object_fields = {"Account": ["password"]}

    for field in filtered_object_fields.get(document_type, []) + all_filtered_fields:
        if hasattr(doc, field):
            doc.pop(field)

    operator_path = f"/{str(operator.id)}" if operator else ""

    publish.single(
        f"/{document_type}/{document.id}/{document_operation}{operator_path}",
        json.dumps(doc),
        hostname=os.environ.get("MQTT_HOST"),
        port=int(os.environ.get("MQTT_PORT")),
    )


def create_event(document, document_operation, operator=None):
    Event.objects.create(
        event=document_operation,
        ref_document=document,
        ref_operator=operator,
    )


def unpack_topic(pattern, topic):
    pattern_parts = pattern.split("/")
    topic_parts = topic.split("/")

    pattern_iter = iter(pattern_parts)
    topic_iter = iter(topic_parts)

    for pattern_part in pattern_iter:
        if pattern_part == "#":
            yield list(topic_iter)
            if next(pattern_iter, None) is not None:
                raise ValueError(
                    "The pattern has a component after a #: {!r}".format(pattern_part)
                )
            return

        try:
            topic_part = next(topic_iter)
        except StopIteration as e:
            raise ValueError(
                "The topic lacks a component to match a non-#-component in the pattern."
            ) from e

        if pattern_part == "+":
            yield topic_part
        elif "+" in pattern_part:
            raise ValueError(
                "The single-level wildcard can be used at any level in the Topic Filter, including first and "
                "last levels. Where it is used, it MUST occupy an entire level of the filter."
            )
        elif "#" in pattern_part:
            raise ValueError(
                "The multi-level wildcard character MUST be specified either on its own or following a topic "
                "level separator. In either case it MUST be the last character specified in the Topic Filter."
            )
        elif pattern_part != topic_part:
            raise ValueError(
                "The pattern {!r} is no wildcard, and the topic {!r} differs.".format(
                    pattern_part, topic_part
                )
            )

    if next(topic_iter, None) is not None:
        raise ValueError(
            "The topic to be matched is longer than the pattern without an # suffix. "
            "The first unmatched part is {!r}".format(next(topic_iter))
        )
