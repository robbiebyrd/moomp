import json
import os

import paho.mqtt.publish as publish

from models.events import Event

ALL_FILTERED_FIELDS = ["_id"]
FILTERED_OBJECT_FIELDS = {"Account": ["password"]}


def notify_and_create_event(
    instance,
    document_type,
    document,
    document_operation,
    operator_type=None,
    operator=None,
):
    create_event(document, document_operation, operator)
    notify(
        instance, document_type, document, document_operation, operator_type, operator
    )


def notify(
    instance,
    document_type,
    document,
    document_operation,
    operator_type=None,
    operator=None,
):
    doc = json.loads(document.to_json(use_db_field=False))

    for field in FILTERED_OBJECT_FIELDS.get(document_type, []) + ALL_FILTERED_FIELDS:
        if hasattr(doc, field):
            doc.pop(field)

    operator_path = f"/{operator_type}/{str(operator.id)}" if operator else ""

    publish.single(
        f"/{instance.id}/{document_type}/{document.id}/{document_operation}{operator_path}",
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


def unpack_topic(pattern: str, topic: str) -> list[str]:
    """Parses and validates MQTT topic patterns with wildcard support.

    This function matches an MQTT topic against a pattern, extracting and validating topic components using single-level
    (+) and multi-level (#) wildcards.

    Args:
        pattern (str): The MQTT topic pattern to match against, which may include '+' or '#' wildcards.
        topic (str): The specific MQTT topic to be parsed and matched.

    Returns:
        list (str): A list of extracted topic components that match the pattern.

    Raises:
        ValueError: If the pattern is invalid or cannot match the topic, with specific error messages for different
        validation scenarios.

    Examples:
        >>> unpack_topic('/123/Character/+/+/Room/+', '/123/Character/456/TeleportedIn/Room/789')
        ['456', 'TeleportedIn', '789']
        >>> unpack_topic('/123/Room/#', '/123/Room/789/TeleportedIn/Character/456')
        ['789', 'TeleportedIn', 'Character', '456']

    Attribution:
        Inspired by decorated-paho-mqtt
        https://github.com/phi1010/decorated-paho-mqtt

        Copyright 2021 Phillip Kuhrt

        Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
        following conditions are met:

        1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
        following disclaimer.

        2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
        following disclaimer in the documentation and/or other materials provided with the distribution.

        3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
        products derived from this software without specific prior written permission.

        THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED
        WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
        PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
        ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
        TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
        HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
        NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY
        OF SUCH DAMAGE.

    """
    pattern_parts = pattern.split("/")
    topic_parts = topic.split("/")

    if "#" in pattern_parts and pattern_parts.index("#") != len(pattern_parts) - 1:
        raise ValueError("Multi-level wildcard '#' must be the last component")

    if len(pattern_parts) > len(topic_parts) and "#" not in pattern_parts:
        raise ValueError("Topic lacks components to match the pattern")

    result = []

    for pattern_part, topic_part in zip(pattern_parts, topic_parts):
        if pattern_part == "#":
            result.extend(topic_parts[len(result) :])
            break
        if pattern_part == "+":
            result.append(topic_part)
        elif pattern_part != topic_part:
            raise ValueError(
                f"Pattern {pattern_part!r} does not match topic {topic_part!r}"
            )

    if len(pattern_parts) < len(topic_parts) and "#" not in pattern_parts:
        raise ValueError(
            f"Topic is longer than pattern. Unmatched part: {topic_parts[len(pattern_parts)]!r}"
        )

    return result


def mqtt_match(topic, wildcard) -> bool:
    """
    Check if an MQTT topic matches a wildcard pattern.

    Args:
        topic (str): The MQTT topic string.
        wildcard (str): The MQTT wildcard pattern.

    Returns:
        bool: True if the topic matches the wildcard, False otherwise.
    """

    if topic == wildcard:
        return True

    topic_parts = topic.split("/")
    wildcard_parts = wildcard.split("/")

    if "#" not in wildcard_parts and len(topic_parts) != len(wildcard_parts):
        return False

    for i in range(len(topic_parts)):
        if wildcard_parts[i] == "+":
            continue
        elif wildcard_parts[i] == "#":
            return True
        elif topic_parts[i] != wildcard_parts[i]:
            return False

    return True
