from .runtimes.wasmer import WasmerRuntime
from .runtimes.wasmtime import WasmtimeRuntime

def apply_operator(image_bytes):
    wasm_file = "../operators/sobel.wasm"
    instance = WasmerRuntime(wasm_file)
    instance.read_image_into_memory(image_bytes)
    instance.apply_operator()
    return instance.retrieve_image()
