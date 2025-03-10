import slack_sdk
import os
from dotenv import load_dotenv
load_dotenv()


class SlackNotifier:

    def __init__(self):
        self.token = os.getenv('SLACK_API_TOKEN')
        self.channel = os.getenv('SLACK_CHANNEL_ID')

    def send_main_message(self, message):
        client = slack_sdk.WebClient(token=self.token)

        return client.chat_postMessage(
            channel=self.channel,
            text=message
        )

    def send_thread_message(self, message, block, thread_ts):
        client = slack_sdk.WebClient(token=self.token)

        return client.chat_postMessage(
            channel=self.channel,
            thread_ts=thread_ts,
            unfurl_links=False,
            text=message,
            blocks=block
        )



