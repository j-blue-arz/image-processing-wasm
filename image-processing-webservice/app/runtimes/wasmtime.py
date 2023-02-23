from wasmtime import WasiConfig, Store, Module, Instance

class WasmtimeRuntime:
    def __init__(self, wasm_file):
        self._store = Store()
        self._store.set_wasi(WasiConfig())
        module = Module.from_file(self._store.engine, wasm_file)
        self._instance = Instance(self._store, module, [])
        self._buffer_pointer = 0
    
    def read_image_into_memory(self, image_bytes):
        buffer_pointer = self._exports("getInputBuffer")(len(image_bytes))
        buffer = self._exports("memory").uint8_view(offset=buffer_pointer)
        buffer[:len(image_bytes)] = image_bytes

    def _exports(self, name):
        return self._instance.exports(self._store)[name]
    
    def apply_operator(self):
        self._buffer_pointer = self._exports("applyImageOperator")()
    
    def retrieve_image(self):
        if self._buffer_pointer != 0:
            size = self._exports("getOutputBufferSize")(self._buffer_pointer)
            buffer = self._exports("memory").uint8_view(offset=self._buffer_pointer)

            return bytes(buffer[:size])
        else:
            print("aborting")