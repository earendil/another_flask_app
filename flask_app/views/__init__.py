from flask import Blueprint

bp = Blueprint('views', __name__)

from views import views
