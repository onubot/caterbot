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
from src.messenger.flows import (
    register,
    index_user,
    login,
    update_state,
    food_confirm_decision,
)
from src.messenger import food_item_list
import pendulum


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
            print(message)
            index_user.update(message)
            user = index_user.get(sender_id)

            # # print(index_user.get(sender_id))
            # if user is None:
            #     return ""

            # Try to grab the quick reply of user
            if user.get("current_state") == State.SCHEDULE_ORDER and not user.get(
                "current_state_completed", False
            ):
                try:
                    quick_reply = message["message"]["quick_reply"]["payload"]
                    scheduled_day = pendulum.now().add(days=1).format("DD-MMM-YYYY")

                    if quick_reply == State.CONFIRM_FOOD_ORDER:
                        mongodb.cx.caterbot.orders.update_one(
                            {"fb_id": sender_id, "scheduled_day": scheduled_day},
                            {"$set": {"state": State.CONFIRM}},
                        )
                        self.send({"text": "অর্ডারটি কনফার্ম করলাম, ধন্যবাদ ^_^"})
                    else:
                        mongodb.cx.caterbot.orders.update_one(
                            {"fb_id": sender_id, "scheduled_day": scheduled_day},
                            {"$set": {"state": State.CANCEL}},
                        )
                        self.send(
                            {
                                "text": "অর্ডারটি ক্যান্সেল করা হল :( , পুনরায় অর্ডার করতে চাইলে দয়া করে আবার Schedule Order থেকে শুরু করুন, ধন্যবাদ!"
                            }
                        )
                except:
                    pass

            if (
                user["current_state"] == State.LOGIN
                and user["current_state_completed"] == False
            ):
                print("FETCHING CREDENTIALS")

                credentials = message["message"]["text"].split(" ")

                if len(credentials) != 2:
                    self.send(
                        {"text": "দয়া করে আবার সঠিকভাবে ইউজারনেম ও পাসওয়ার্ড দিন"},
                        "RESPONSE",
                    )

                # return None
                else:

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
                                "text": f"অভিনন্দন {username}, আপনি সিস্টেমে লগিন করতে পেরেছেন, আপনি চাইলে আগামীকালের জন্য এখনি অর্ডার করতে পারেন :D"
                            }
                        )

                    else:
                        self.send(
                            {
                                "text": "দুঃখিত, আপনার ইউজারনেম বা পাসওয়ার্ডটি ভুল। দয়া করে আবার ট্রাই করুন। "
                            }
                        )

                # else:
                #     self.send(
                #         {
                #             "text": "আপনি লগডইন অবস্থায়ই আছেন, চাইলে আগামীকালের জন্য অর্ডার প্লেস করুন। ধন্যবাদ।"
                #         }
                #     )

    def delivery(self, message):
        pass

    def read(self, message):
        pass

    def account_linking(self, message):
        pass

    def postback(self, message):
        print("postback", message)

        user = index_user.get(message["sender"]["id"]) or {}

        # User not found, better index him at first
        if user == {}:
            index_user.index(message)

        if message["postback"]["payload"] == State.SCHEDULE_ORDER:
            if not user.get("logged_in", False):
                self.send({"text": "অর্ডার করার জন্য দয়া করে লগিন করুন। ধন্যবাদ"})
            else:
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

        if "ORDER#" in message["postback"]["payload"]:
            update_state.update(
                user.get("fb_id", None),
                current_state=State.SCHEDULE_ORDER,
                state_completion=False,
            )

            item_id = message["postback"]["payload"].split("ORDER#")[-1]
            # print(item_id)
            item = [
                f for f in food_item_list.food_list["foods"] if f["food_id"] == item_id
            ][0]

            scheduled_day = pendulum.now().add(days=1).format("DD-MMM-YYYY")

            mongodb.cx.caterbot.orders.update_one(
                {"userId": user.get("fb_id", None), "scheduled_day": scheduled_day},
                update={
                    "$set": {
                        "userId": user.get("fb_id", None),
                        "item": item,
                        "scheduled_day": scheduled_day,
                        "state": State.PENDING,
                    }
                },
                upsert=True,
            )

            self.send(food_confirm_decision.get_confirmation(item), "RESPONSE")

        if message["postback"]["payload"] == State.LOGIN:
            if message["sender"]["id"] != PAGE_ID:

                if user.get("logged_in", False):
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
        # print(message)
        pass
