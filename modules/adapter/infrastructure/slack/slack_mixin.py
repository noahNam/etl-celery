import os

import requests


class SlackMixin:
    def send_slack_message(self, title: str, message: str):
        text = title + "\n" + message
        slack_token = os.environ.get("SLACK_TOKEN")
        slack_channel = os.environ.get("SLACK_CHANNEL")
        if slack_token:
            requests.post(
                "https://slack.com/api/chat.postMessage",
                headers={"Authorization": "Bearer " + slack_token},
                data={"channel": slack_channel, "text": text},
            )
