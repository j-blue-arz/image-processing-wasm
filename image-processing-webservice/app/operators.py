import glob
import re
import os

from flask import current_app, abort

from .runtimes.wasmer import WasmerRuntime
from .runtimes.wasmtime import WasmtimeRuntime
from .runtimes.extism import ExtismRuntime

_RUNTIMES = {
    "wasmer": WasmerRuntime,
    "wasmtime": WasmtimeRuntime,
    "extism": ExtismRuntime
}

def apply_operator(image_bytes, operator, runtime):
    wasm_file = _find_matching_operator(operator, runtime)
    instance = _RUNTIMES[runtime](wasm_file)
    return instance.apply_operator(image_bytes)

def fetch_operators(with_paths=False):
    folder = current_app.config["OPERATORS_PATH"]
    file_paths = glob.glob(os.path.join(folder, '*.wasm'))
    response = [
        {
            "name": re.sub(r"_extism$", "", _file_name(file_path)),
            "runtime": "extism" if _file_name(file_path).endswith("_extism") else "wasmtime"
        } | 
        ({"path": file_path} if with_paths else {})
        for file_path in file_paths
    ]
    return response

def _file_name(path):
    return os.path.splitext(os.path.basename(path))[0]

def _find_matching_operator(operator, interface):
    available_operators = fetch_operators(with_paths=True)
    name_matches = [op for op in available_operators if op["name"] == operator]
    full_match = [op for op in name_matches if op["runtime"] == interface]
    if not full_match:
        abort(404)
    return full_match[0]["path"]
