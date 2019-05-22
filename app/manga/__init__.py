from flask import Blueprint

manga = Blueprint('manga', __name__)

from . import routes, forms
