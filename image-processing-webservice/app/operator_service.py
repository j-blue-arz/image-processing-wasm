from flask import Blueprint

from . import operators

API = Blueprint("operator_api", __name__, url_prefix="/api/operators")

@API.route("")
def get_operators():
    return operators.fetch_operators()