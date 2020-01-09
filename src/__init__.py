from flask import Flask
from src import db
from flask_cors import CORS
import config

def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = f"mongodb://{config.mongo_host}:27017/caterbot"
    db.mongodb.init_app(app)

    CORS(app)

    from src.auth import auth as auth_blueprint
    from src.dashboard import dash as dash_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(dash_blueprint)

    return app
