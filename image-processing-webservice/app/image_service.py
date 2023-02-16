from flask import Blueprint, request
from operators import apply_operator

API = Blueprint("api", __name__, url_prefix='/api')

@API.route("/process-image", methods=["POST"])
def process_image():
    imagefile = request.files['imagefile']
    result = apply_operator(imagefile.read())

