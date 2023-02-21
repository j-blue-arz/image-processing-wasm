from flask import Blueprint, request, make_response
from . import operators

import gc
import os
import tracemalloc
import psutil

API = Blueprint("api", __name__, url_prefix="/api")

process = psutil.Process(os.getpid())
tracemalloc.start()
s = None

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

@API.route('/memory')
def print_memory():
    return {'memory': process.memory_info().rss}


@API.route("/snapshot")
def snap():
    global s
    if not s:
        s = tracemalloc.take_snapshot()
        return "taken snapshot\n"
    else:
        lines = []
        j = tracemalloc.take_snapshot()
        top_stats = j.compare_to(s, 'lineno')
        for stat in top_stats[:5]:
            lines.append(str(stat))
        s = j
        return "\n".join(lines)