from src.auth import auth
from flask import jsonify, request
import os
from src import db
from src.messenger import handle_message

@auth.route("/webhook", methods=["GET", "POST"])
def auth_webhook():
    if request.method == "GET":
        if (request.args.get("hub.verify_token") == os.environ.get("FB_VERIFY_TOKEN")):
            return request.args.get("hub.challenge")
        raise ValueError("FB_VERIFY_TOKEN does not match")
    if request.method == "POST":
        handle_message(request.get_json(force=True))
    return ''
        


@auth.route("/auth", methods=["GET"])
def get_auth():
    print(list(db.mongodb.cx.list_databases()))
    return jsonify({"Hello" : "world"})