Wasmer with cranelift takes about 2.8s on top-end notebook. About 44% of that time is creating the instance. This part could be cached.
There is a memory leak somewhere. Between requests, about 200MB of memory is leaked! Maybe the instance is not cleaned up correctly.
seems to be in line

`module = Module(store, wasm_bytes)`

Wasmtime takes about 1.1s for sobel on skyscraper image
Extism is slower, takes about 2s for same image.
Wasmtime is low level, Extism has convenient I/O API for handle byte arrays.


## Versions

tinygo >= 0.28.0 with go 1.21/1.20/1.19 fails at runtime due to a panic in `compress/zlib.Writer`. Both with wasmtime and with Extism.

tinygo 0.26.0 with go 1.19 does not have that problem. Running with wasmtime-python works fine both for 8.0 and for 14.0. But it fails to build with Go PDK v1.0.0-rc1 (extism library 0.5.0 and v1.0.0).
errors like `undefined symbol: github.com/extism/go-pdk.extism_free`. The reason is that support for `//go:wasmimport` was only added in tinygo 0.28.0.

Another option would be to downgrade Go PDK and extism to some older version.

'Solved' by using `jpeg.Encode` instead of `png.Encode`.

Also, on server-side, Extism Python SDK version has to match the installed Extism library version. 0.5.0 is the latest Extism Python SDK as of now.

