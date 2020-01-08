from fbmessenger import BaseMessenger, MessengerClient
import os
from pprint import pprint
from src.db import mongodb
from src.states import State
import datetime
from src.messenger.flows import register, index_user

PAGE_ID = "619830321739930"


class Messenger(BaseMessenger):
    def __init__(self, app_secret=None):
        self.page_access_token = os.environ.get("FB_PAGE_TOKEN")
        self.app_secret = app_secret
        self.client = MessengerClient(
            self.page_access_token, app_secret=self.app_secret
        )

    def message(self, message):
        if message["sender"]["id"] != PAGE_ID:
            index_user.update(message)
            print(message)
            self.send(
                {"text": "Received: {0}".format(message["message"]["text"])}, "RESPONSE"
            )

    def delivery(self, message):
        pass

    def read(self, message):
        pass

    def account_linking(self, message):
        pass

    def postback(self, message):
        # mongodb.cx.caterbot.user.update_one()
        print("postback", message)

        if message["postback"]["payload"] == State.REGISTER:
            pass

        if message["postback"]["payload"] == State.HI:
            if message["sender"]["id"] != PAGE_ID:
                index_user.index(message)

    def optin(self, message):
        pass
