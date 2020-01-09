# Dashboard blueprint
from flask.blueprints import Blueprint
from config import api_version

dash = Blueprint(__name__, 'dash', url_prefix=f"/api/{api_version}/dashboard")

from . import views