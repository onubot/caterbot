from src.auth import auth
from flask import jsonify
from src import db

@auth.route("/auth/webhook")

@auth.route("/auth", methods=["GET"])
def get_auth():
    print(list(db.mongodb.cx.list_databases()))
    return jsonify({"Hello" : "world"})