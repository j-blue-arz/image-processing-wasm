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
    gc.collect()
    return response

@API.route("/pstats")
def pstats():
    process = psutil.Process(os.getpid())
    return {
        "rss": f"{process.memory_info().rss / 1024 ** 2:.2f} MiB",
        "vms": f"{process.memory_info().vms / 1024 ** 2:.2f} MiB",
        "shared": f"{process.memory_info().shared / 1024 ** 2:.2f} MiB",
        "open file descriptors": process.num_fds(),
        "threads": process.num_threads(),
    }


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