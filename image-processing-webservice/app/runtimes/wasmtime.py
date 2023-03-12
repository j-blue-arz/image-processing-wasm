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
    
    def read_image_into_memory(self, image_bytes):
        buffer_pointer = self._call_func("getInputBuffer", len(image_bytes))
        self._set_slice(image_bytes, buffer_pointer)
    
    def apply_operator(self):
        self._buffer_pointer = self._call_func("applyImageOperator")
    
    def retrieve_image(self):
        if self._buffer_pointer != 0:
            size = self._call_func("getOutputBufferSize", self._buffer_pointer)
            return self._get_slice(slice(self._buffer_pointer, self._buffer_pointer+size))
        else:
            print("aborting")
    
    def _call_func(self, name, *args):
        return self._exports(name)(self._store, *args)

    def _exports(self, name):
        return self._instance.exports(self._store)[name]
    
    # see https://github.com/bytecodealliance/wasmtime-py/issues/81
    def _set_slice(self, val, start=0, end=None):
        memory_ptr = self._exports("memory").data_ptr(self._store)
        size = self._exports("memory").data_len(self._store)
        val_size = len(val)
        if end is None: end=start+val_size
        if end-start>val_size or end>size:
            raise IndexError("out of memory size")
        src_ptr = (ctypes.c_ubyte * val_size).from_buffer(bytearray(val))
        dst_ptr = ctypes.addressof((ctypes.c_ubyte*val_size).from_address(ctypes.addressof(memory_ptr.contents)+start))
        ctypes.memmove(dst_ptr, src_ptr, val_size)
        return
    
    # see https://github.com/bytecodealliance/wasmtime-py/pull/134
    def _get_slice(self, key):
        data_ptr = self._exports("memory").data_ptr(self._store)
        size = self._exports("memory").data_len(self._store)
        start = key.start
        stop = key.stop

        val_size = stop - start
        value = bytearray(val_size)

        if stop is None:
            stop = start+val_size
        if stop>size:
            raise IndexError("out of memory size")
        dst_ptr = (ctypes.c_ubyte * val_size).from_buffer(value)
        src_ptr = ctypes.addressof((ctypes.c_ubyte*val_size).from_address(ctypes.addressof(data_ptr.contents)+start))
        ctypes.memmove(dst_ptr, src_ptr, val_size)
        return value