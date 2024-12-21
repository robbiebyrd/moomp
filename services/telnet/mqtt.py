from mongoengine import Q

from models.object import Object
from utils.db import connect_db

connect_db()


def current_subscriptions(session):
    # The character always subscribes to their own events
    subscriptions = [f"/{session.instance.id}/Character/{session.character.id}/#"]

    # If a character is in a room, then it subscribes to that room's events
    if session.character.room:
        subscriptions.extend(
            (
                f"/{session.instance.id}/Room/{session.character.room.id}/#",
                f"/{session.instance.id}/Speech/+/Room/{session.character.room.id}/#",
            )
        )

    # If a user is holding any objects, then receive event updates on those
    subscriptions.extend(
        f"/{session.instance.id}/Object/{obj.id}/#"
        for obj in Object.objects(
            Q(holder=session.character.id) | Q(room=session.character.room.id)
        )
    )

    return subscriptions


async def subscribe(session, subscriptions):
    if isinstance(subscriptions, str):
        subscriptions = [subscriptions]

    for subscription in subscriptions:
        session.mqtt_client.subscribe(subscription)


async def unsubscribe(session, subscriptions):
    if isinstance(subscriptions, str):
        subscriptions = [subscriptions]

    for subscription in subscriptions:
        session.mqtt_client.unsubscribe(subscription)


async def refresh_subscriptions(session):
    topics_to_subscribe = current_subscriptions(session)
    session.message_topics = list(set(session.message_topics + topics_to_subscribe))

    topics_to_unsubscribe = [
        subscription
        for subscription in session.message_topics
        if subscription not in topics_to_subscribe
    ]
    for topic_to_unsubscribe in topics_to_unsubscribe:
        session.message_topics.remove(topic_to_unsubscribe)

    await subscribe(session, topics_to_subscribe)
    await unsubscribe(session, topics_to_unsubscribe)
    session.mqtt_client.user_data_set(session)
