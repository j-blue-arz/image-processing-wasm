from wasmtime import WasiConfig, Store, Module, Instance

class WasmtimeRuntime:
    def __init__(self, wasm_file):
        store = Store()
        store.set_wasi(WasiConfig())
        module = Module.from_file(store.engine, wasm_file)
        self._instance = Instance(store, module, [])
        self._buffer_pointer = 0
    
    def read_image_into_memory(self, image_bytes):
        buffer_pointer = self._instance.exports.getInputBuffer(len(image_bytes))
        buffer = self._instance.exports.memory.uint8_view(offset=buffer_pointer)
        buffer[:len(image_bytes)] = image_bytes
    
    def apply_operator(self):
        self._buffer_pointer = self._instance.exports.applyImageOperator()
    
    def retrieve_image(self):
        if self._buffer_pointer != 0:
            size = self._instance.exports.getOutputBufferSize(self._buffer_pointer)
            buffer = self._instance.exports.memory.uint8_view(offset=self._buffer_pointer)

            return bytes(buffer[:size])
        else:
            print("aborting")