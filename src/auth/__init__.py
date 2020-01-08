from flask.blueprints import Blueprint
from config import api_version

auth = Blueprint(__name__, 'auth', url_prefix=f"/api/{api_version}/auth")

from . import views