from wasmer import engine, wasi, Store, Module, Instance
from wasmer_compiler_cranelift import Compiler

with open("../operators/sobel/sobel.wasm", "rb") as f:
    wasm_bytes = f.read()

store = Store(engine.Universal(Compiler))
module = Module(store, wasm_bytes)

wasi_version = wasi.get_version(module, strict=True)

wasi_env = wasi.StateBuilder("image-processor").finalize()

import_object = wasi_env.generate_import_object(store, wasi_version)

instance = Instance(module, import_object)

with open("skyline.jpg", "rb") as f:
    image_bytes = f.read()

buffer_pointer = instance.exports.getInputBuffer(len(image_bytes))
buffer = instance.exports.memory.uint8_view(offset=buffer_pointer)
buffer[:len(image_bytes)] = image_bytes

buffer_pointer = instance.exports.applySobelOperator()
if buffer_pointer != 0:
    size = instance.exports.getOutputBufferSize(buffer_pointer)
    buffer = instance.exports.memory.uint8_view(offset=buffer_pointer)

    image_bytes = bytes(buffer[:size])

    with open("output.png", "wb") as f:
        f.write(image_bytes)
else:
    print("aborting")
