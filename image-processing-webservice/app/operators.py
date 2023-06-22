from .runtimes.wasmer import WasmerRuntime
from .runtimes.wasmtime import WasmtimeRuntime
from .runtimes.extism import ExtismRuntime

def apply_operator(image_bytes):
    wasm_file = "../operators/sobel.wasm"
    instance = WasmtimeRuntime(wasm_file)
    return instance.apply_operator(image_bytes)
