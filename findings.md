Wasmer with cranelift takes about 2.8s on top-end notebook. About 44% of that time is creating the instance. This part could be cached.
There is a memory leak somewhere. Between requests, about 200MB of memory is leaked! Maybe the instance is not cleaned up correctly.
seems to be in line

`module = Module(store, wasm_bytes)`