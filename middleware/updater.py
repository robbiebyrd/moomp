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
    # Make a shallow copy of the document object for filtering.
    doc = json.loads(document.to_json())

    private_fields = {"Character": ["password"]}

    for field in private_fields.get(document_type, []):
        if hasattr(doc, field):
            doc.pop(field)

    operator_path = ("/" + str(operator.id)) if operator else ""

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
    """
    returns one string for each "+", followed by a list of strings when a trailing "#" is present
    """
    pattern_parts = iter(pattern.split("/"))
    topic_parts = iter(topic.split("/"))
    while True:
        try:
            cur_pattern = next(pattern_parts)
        except StopIteration:
            try:
                cur_topic = next(topic_parts)
                raise Exception(
                    "The topic to be matched is longer than the pattern without an # suffix. "
                    "The first unmatched part is {!r}".format(cur_topic)
                )
            except StopIteration:
                # no more elements in both sequences.
                return
        if cur_pattern == "#":
            yield list(topic_parts)
            try:
                cur_pattern = next(pattern_parts)
                raise Exception("The pattern has a component after a #: {!r}".format(cur_pattern))
            except StopIteration:
                # topic has been exhausted by list() enumeration, and pattern is empty, too.
                return
        else:
            try:
                cur_topic = next(topic_parts)
            except StopIteration:
                raise Exception("The topic lacks a component to match a non-#-component in the pattern.")
            else:
                if cur_pattern == "+":
                    yield cur_topic
                elif "+" in cur_pattern:
                    raise Exception(
                        "The single-level wildcard can be used at any level in the Topic Filter, including first and last levels. Where it is used, it MUST occupy an entire level of the filter."
                    )
                elif "#" in cur_pattern:
                    raise Exception(
                        "The multi-level wildcard character MUST be specified either on its own or following a topic level separator. In either case it MUST be the last character specified in the Topic Filter."
                    )
                elif cur_pattern != cur_topic:
                    raise Exception(
                        "The pattern {!r} is no wildcard, and the topic {!r} differs.".format(cur_pattern, cur_topic)
                    )
                else:  # pattern == topic and neither contain a # or +
                    # we do not yield return constant non-wildcards.
                    continue
