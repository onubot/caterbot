from fbmessenger import BaseMessenger, MessengerClient
from fbmessenger.elements import Element
from fbmessenger import elements
from fbmessenger import templates
from fbmessenger.templates import ListTemplate
import os
from pprint import pprint
from src.db import mongodb
from src.states import State
import datetime
from src.messenger.flows import register, index_user, login, update_state
from src.messenger import food_item_list


PAGE_ID = "619830321739930"


class Messenger(BaseMessenger):
    def __init__(self, app_secret=None):
        self.page_access_token = os.environ.get("FB_PAGE_TOKEN")
        self.app_secret = app_secret
        self.client = MessengerClient(
            self.page_access_token, app_secret=self.app_secret
        )

    def message(self, message):
        sender_id = message["sender"]["id"]

        if sender_id != PAGE_ID:
            index_user.update(message)
            user = index_user.get(sender_id)

            print(index_user.get(sender_id))

            if (
                user["current_state"] == State.LOGIN
                and user["current_state_completed"] == False
            ):
                credentials = message["message"]["text"].split(" ")
                if len(credentials) != 2:
                    self.send(
                        {"text": "দয়া করে আবার সঠিকভাবে ইউজারনেম ও পাসওয়ার্ড দিন"},
                        "RESPONSE",
                    )

                username, password = credentials

                if username == user["username"] and password == user["password"]:
                    update_state.update(
                        sender_id,
                        current_state=State.LOGIN,
                        state_completion=True,
                        logged_in=True,
                    )
                    self.send(
                        {
                            "text": f"অভিনন্দন {username}, আপনি সিস্টেমে লগিন করতে পেরেছেন, আপনি চাইলে আগামীকালের জন্য এখনি অর্ডার করতে পারেন"
                        }
                    )

                else:
                    self.send(
                        {
                            "text": "দুঃখিত, আপনার ইউজারনেম বা পাসওয়ার্ডটি ভুল। দয়া করে আবার ট্রাই করুন।"
                        }
                    )

            else:
                self.send(
                    {
                        "text": "আপনি লগডইন অবস্থায়ই আছেন, চাইলে আগামীকালের জন্য অর্ডার প্লেস করুন। ধন্যবাদ।"
                    }
                )

            print(message)

    def delivery(self, message):
        pass

    def read(self, message):
        pass

    def account_linking(self, message):
        pass

    def postback(self, message):
        print("postback", message)

        if message["postback"]["payload"] == State.SCHEDULE_ORDER:
            self.send(
                templates.GenericTemplate(
                    elements=food_item_list.food_elements,
                ).to_dict(),
                "RESPONSE",
            )


        if message["postback"]["payload"] == State.REGISTER:
            pass

        if message["postback"]["payload"] == State.HI:
            if message["sender"]["id"] != PAGE_ID:
                index_user.index(message)

        if message["postback"]["payload"] == State.LOGIN:
            if message["sender"]["id"] != PAGE_ID:
                user = index_user.get(message["sender"]["id"])

                if user["logged_in"]:
                    self.send(
                        {
                            "text": "আপনি লগড-ইন অবস্থায়ই আছেন, চাইলে আগামীকালের জন্য অর্ডার প্লেস করুন। ধন্যবাদ।"
                        }
                    )

                else:
                    update_state.update(
                        message["sender"]["id"],
                        current_state=State.LOGIN,
                        state_completion=False,
                    )
                    self.send(
                        {
                            "text": "দয়া করে ইউজারনেম ও পাসওয়ার্ড দিন, উদাহরণ: username password"
                        },
                        "RESPONSE",
                    )

    def optin(self, message):
        pass
