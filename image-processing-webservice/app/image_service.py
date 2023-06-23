from flask import Blueprint, request, make_response
from . import operators

import os
import time
import tracemalloc
import psutil

API = Blueprint("image", __name__, url_prefix="/api")

process = psutil.Process(os.getpid())
tracemalloc.start()
s = None

timings = []

@API.route("/process-image", methods=["POST"])
def process_image():
    start = time.time()
    imagefile = request.files["image"]
    image_bytes = operators.apply_operator(imagefile.read(), request.form["operator_name"], request.form["operator_runtime"])
    response = make_response(image_bytes)
    response.headers.set("Content-Type", "image/png")
    diff = time.time() - start
    timings.append(diff)
    return response

@API.route("/timings")
def get_timings():
    return {"timings": timings}