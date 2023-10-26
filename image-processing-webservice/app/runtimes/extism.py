from extism import Plugin

class ExtismRuntime:
    def __init__(self, wasm_file):
        with open(wasm_file, "rb") as f:
            wasm_bytes = f.read()
        config = {"wasm": [{"data": wasm_bytes}]}
        self._plugin = Plugin(config, wasi=True)
    
    def __del__(self):
        del self._plugin
    
    def apply_operator(self, image_bytes):
        return self._plugin.call("applyImageOperator", image_bytes)
