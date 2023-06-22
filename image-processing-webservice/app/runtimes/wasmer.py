from wasmer import engine, wasi, Store, Module, Instance
from wasmer_compiler_cranelift import Compiler

class WasmerRuntime:
    def __init__(self, wasm_file):
        with open(wasm_file, "rb") as f:
            wasm_bytes = f.read()
        store = Store(engine.Universal(Compiler))
        module = Module(store, wasm_bytes)
        wasi_version = wasi.get_version(module, strict=True)
        wasi_env = wasi.StateBuilder("image-processor").finalize()
        import_object = wasi_env.generate_import_object(store, wasi_version)
        self._instance = Instance(module, import_object)
        self._buffer_pointer = 0
    
    def apply_operator(self, image_bytes):
        self._read_image_into_memory(image_bytes)
        self._apply_operator_on_image()
        return self._retrieve_image()
    
    def _read_image_into_memory(self, image_bytes):
        buffer_pointer = self._instance.exports.getInputBuffer(len(image_bytes))
        buffer = self._instance.exports.memory.uint8_view(offset=buffer_pointer)
        buffer[:len(image_bytes)] = image_bytes
    
    def _apply_operator_on_image(self):
        self._buffer_pointer = self._instance.exports.applyImageOperator()
    
    def _retrieve_image(self):
        if self._buffer_pointer != 0:
            size = self._instance.exports.getOutputBufferSize(self._buffer_pointer)
            buffer = self._instance.exports.memory.uint8_view(offset=self._buffer_pointer)

            return bytes(buffer[:size])
        else:
            print("aborting")