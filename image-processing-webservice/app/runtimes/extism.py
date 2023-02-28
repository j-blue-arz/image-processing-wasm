import hashlib

from extism import Context

class ExtismRuntime:
    def __init__(self, wasm_file):
        with open(wasm_file, "rb") as f:
            wasm_bytes = f.read()
        hash = hashlib.sha256(wasm_bytes).hexdigest()
        self._ctx = Context()
        config = {"wasm": [{"data": wasm_bytes, "hash": hash}], "memory": {"max": 64}}
        self._plugin = self._ctx.plugin(config, wasi=True)
        self._buffer_pointer = 0
    
    def __del__(self):
        del self._ctx
        del self._plugin
    
    def read_image_into_memory(self, image_bytes):
        buffer_pointer = self._plugin.call("getInputBuffer", len(image_bytes))
        buffer = self._exports("memory").uint8_view(offset=buffer_pointer)
        buffer[:len(image_bytes)] = image_bytes
    
    def apply_operator(self):
        self._buffer_pointer = self._plugin.call("applyImageOperator")
    
    def retrieve_image(self):
        if self._buffer_pointer != 0:
            size = self._plugin.call("getOutputBufferSize", self._buffer_pointer)
            buffer = self._plugin.memory_at_offset _exports("memory").uint8_view(offset=self._buffer_pointer)

            return bytes(buffer[:size])
        else:
            print("aborting")