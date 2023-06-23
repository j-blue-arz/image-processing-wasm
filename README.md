# Image Processing webapp with user-provided plugins

This is a toy project, experimenting with a WebAssembly plugin architecture.
* Developer can implement and upload image operators in WebAssembly format.
* User can apply operators on an image.

## Roadmap
- [x] apply sobel operator in Python with Wasmer
- [x] Provide REST-API with Flask
- [ ] Investigate memory leak -> Could not solve it.
- [X] try Wasmtime and Extism
- [X] Add webclient
- [ ] Add selector for runtime
- [ ] Add selector for image operators
- [ ] Add dynamic upload of image operators
- [ ] Docker build