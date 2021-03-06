from src.db import mongodb
from src.states import State


def get(id):
    return mongodb.cx.caterbot.user.find_one({"fb_id": id})


def update(message):
    mongodb.cx.caterbot.user.update_one(
        {"fb_id": message["sender"]["id"]},
        {"$set": {"last_message": message["message"]}},
    )


def index(message):
    if not mongodb.cx.caterbot.user.find_one({"fb_id": message["sender"]["id"]}):
        mongodb.cx.caterbot.user.insert_one(
            {
                "fb_id": message["sender"]["id"],
                "registered": True,
                "last_state": None,
                "current_state": State.HI,
                "last_state_completed": False,
                "current_state_completed": True,
                "daily_reminder_time": "9PM",
                "username": "abc",
                "password": "def",
                "logged_in" : False,
                "last_message": "",
            }
        )

