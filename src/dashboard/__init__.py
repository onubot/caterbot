# Dashboard blueprint
from flask.blueprints import Blueprint
from config import api_version

dash = Blueprint(
    "dashboard",
    __name__,
    url_prefix=f"/api/{api_version}/dashboard",
    template_folder="templates/dashboard",
)

from . import views
