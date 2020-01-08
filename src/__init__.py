from flask import Flask
from src import db


def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/caterbot"
    db.mongodb.init_app(app)

    from src.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app