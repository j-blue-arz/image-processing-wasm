package main

import (
	"bytes"
	"image/jpeg"
	"unsafe"
)

var inputBuffer []byte
var outputBuffer []byte

//go:export applyImageOperator
func applyImageOperator() uintptr {
	img, err := jpeg.Decode(bytes.NewReader(inputBuffer))
	if err != nil {
		println(err.Error())
		return 0
	}
	resultImage := sobel(img)
	var byteBuffer bytes.Buffer
	jpeg.Encode(&byteBuffer, resultImage, nil)
	outputBuffer = byteBuffer.Bytes()

	return arrayToPtr(outputBuffer)
}

//go:export getInputBuffer
func getInputBuffer(size uint32) uintptr {
	inputBuffer = make([]byte, size)
	return arrayToPtr(inputBuffer)
}

//go:export getOutputBufferSize
func getOutputBufferSize(ptr uintptr) uint32 {
	if arrayToPtr(outputBuffer) == ptr {
		return uint32(len(outputBuffer))
	} else if arrayToPtr(inputBuffer) == ptr {
		return uint32(len(inputBuffer))
	} else {
		return 0
	}
}

func arrayToPtr(array []byte) uintptr {
	ptr := &array[0]
	return uintptr(unsafe.Pointer(ptr))
}

func main() {}
