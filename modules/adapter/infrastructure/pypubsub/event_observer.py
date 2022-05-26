from pubsub import pub


def send_message(topic_name: str | None = None, **kwargs):
    pub.sendMessage(topicName=topic_name, **kwargs)
