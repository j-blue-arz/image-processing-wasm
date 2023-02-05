from wasmer import engine, wasi, Store, Module, Instance
from wasmer_compiler_cranelift import Compiler

instance = None

def get_instance():
    global instance
    if not instance:
        with open("../operators/sobel/sobel.wasm", "rb") as f:
            wasm_bytes = f.read()

        store = Store(engine.Universal(Compiler))
        module = Module(store, wasm_bytes)

        wasi_version = wasi.get_version(module, strict=True)

        wasi_env = wasi.StateBuilder("image-processor").finalize()

        import_object = wasi_env.generate_import_object(store, wasi_version)

        instance = Instance(module, import_object)
    return instance

def read_image():
    with open("skyline.jpg", "rb") as f:
        image_bytes = f.read()

    buffer_pointer = get_instance().exports.getInputBuffer(len(image_bytes))
    buffer = get_instance().exports.memory.uint8_view(offset=buffer_pointer)
    buffer[:len(image_bytes)] = image_bytes

def write_image(buffer_pointer):
    if buffer_pointer != 0:
        size = get_instance().exports.getOutputBufferSize(buffer_pointer)
        buffer = get_instance().exports.memory.uint8_view(offset=buffer_pointer)

        image_bytes = bytes(buffer[:size])

        with open("output.png", "wb") as f:
            f.write(image_bytes)
    else:
        print("aborting")

read_image()
buffer_pointer = get_instance().exports.applyImageOperator()
write_image(buffer_pointer)
