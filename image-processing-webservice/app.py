import sys

from wasmer import engine, wasi, Store, Module, Instance
from wasmer_compiler_cranelift import Compiler

def create_instance(wasm_file):
    with open(wasm_file, "rb") as f:
        wasm_bytes = f.read()

    store = Store(engine.Universal(Compiler))
    module = Module(store, wasm_bytes)

    wasi_version = wasi.get_version(module, strict=True)

    wasi_env = wasi.StateBuilder("image-processor").finalize()

    import_object = wasi_env.generate_import_object(store, wasi_version)

    return Instance(module, import_object)

def read_image(instance):
    with open("skyline.jpg", "rb") as f:
        image_bytes = f.read()

    buffer_pointer = instance.exports.getInputBuffer(len(image_bytes))
    buffer = instance.exports.memory.uint8_view(offset=buffer_pointer)
    buffer[:len(image_bytes)] = image_bytes

def write_image(instance, buffer_pointer):
    if buffer_pointer != 0:
        size = instance.exports.getOutputBufferSize(buffer_pointer)
        buffer = instance.exports.memory.uint8_view(offset=buffer_pointer)

        image_bytes = bytes(buffer[:size])

        with open("output.png", "wb") as f:
            f.write(image_bytes)
    else:
        print("aborting")

if __name__ == "__main__":
    wasm_file = sys.argv[1] if len(sys.argv) > 1 else "../operators/noop.wasm"
    instance = create_instance(wasm_file)
    read_image(instance)
    buffer_pointer = instance.exports.applyImageOperator()
    write_image(instance, buffer_pointer)
