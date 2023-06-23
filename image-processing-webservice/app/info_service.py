from flask import Blueprint

import os
import tracemalloc
import psutil

API = Blueprint("info", __name__, url_prefix="/api/info")

@API.route("")
def version():
    return {"version": "0.1.0"}

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

