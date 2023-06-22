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
    
    def apply_operator(self, image_bytes):
        return self._plugin.call("applyImageOperator", image_bytes)
    
