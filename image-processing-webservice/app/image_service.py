from flask import Blueprint, request, make_response
from . import operators

API = Blueprint("api", __name__, url_prefix="/api")


@API.route("/info", methods=["GET"])
def version():
    return {"version": "0.1.0"}


@API.route("/process-image", methods=["POST"])
def process_image():
    imagefile = request.files["image"]
    image_bytes = operators.apply_operator(imagefile.read())
    response = make_response(image_bytes)
    response.headers.set("Content-Type", "image/png")
    return response
