import ctypes

from wasmtime import WasiConfig, Store, Module, Instance, Linker, Engine

class WasmtimeRuntime:
    def __init__(self, wasm_file):
        linker = Linker(Engine())
        linker.define_wasi()
        self._store = Store(linker.engine)
        self._store.set_wasi(WasiConfig())
        module = Module.from_file(self._store.engine, wasm_file)
        self._instance = linker.instantiate(self._store, module)
        self._buffer_pointer = 0
    
    def apply_operator(self, image_bytes):
        self._read_image_into_memory(image_bytes)
        self._apply_operator_on_image()
        return self._retrieve_image()
    
    def _read_image_into_memory(self, image_bytes):
        buffer_pointer = self._call_func("getInputBuffer", len(image_bytes))
        self._exports("memory").write(self._store, image_bytes, buffer_pointer)
    
    def _apply_operator_on_image(self):
        self._buffer_pointer = self._call_func("applyImageOperator")
    
    def _retrieve_image(self):
        if self._buffer_pointer != 0:
            size = self._call_func("getOutputBufferSize", self._buffer_pointer)
            return self._exports("memory").read(self._store, self._buffer_pointer, self._buffer_pointer+size)
        else:
            print("aborting")
    
    def _call_func(self, name, *args):
        return self._exports(name)(self._store, *args)

    def _exports(self, name):
        return self._instance.exports(self._store)[name]
    