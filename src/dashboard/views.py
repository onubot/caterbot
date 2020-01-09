from src.dashboard import dash
from flask import jsonify
from src.db import mongodb


@dash.route("/orders", methods=["GET"])
def fetch_orders():
    data = list(
        mongodb.cx.caterbot.orders.find(
            {},
            {
                "_id": 0,
                "scheduled_day": 1,
                "state": 1,
                "item.title": 1,
                "item.price": 1,
                "userId": 1,
            },
        )
    )
    return {"data": data}

