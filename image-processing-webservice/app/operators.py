import sys

from wasmer import engine, wasi, Store, Module, Instance
from wasmer_compiler_cranelift import Compiler

def _create_instance(wasm_file):
    with open(wasm_file, "rb") as f:
        wasm_bytes = f.read()

    store = Store(engine.Universal(Compiler))
    module = Module(store, wasm_bytes)

    wasi_version = wasi.get_version(module, strict=True)

    wasi_env = wasi.StateBuilder("image-processor").finalize()

    import_object = wasi_env.generate_import_object(store, wasi_version)

    return Instance(module, import_object)

def _read_image(instance, image_bytes):
    buffer_pointer = instance.exports.getInputBuffer(len(image_bytes))
    buffer = instance.exports.memory.uint8_view(offset=buffer_pointer)
    buffer[:len(image_bytes)] = image_bytes

def _fetch_image(instance, buffer_pointer):
    if buffer_pointer != 0:
        size = instance.exports.getOutputBufferSize(buffer_pointer)
        buffer = instance.exports.memory.uint8_view(offset=buffer_pointer)

        return bytes(buffer[:size])
    else:
        print("aborting")

def apply_operator(image_bytes):
    wasm_file = "../operators/sobel.wasm"
    instance = _create_instance(wasm_file)
    _read_image(instance, image_bytes)
    buffer_pointer = instance.exports.applyImageOperator()
    return _fetch_image(instance, buffer_pointer)
