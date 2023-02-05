package main

import (
	"unsafe"
)

var buffer []byte

//go:export applyImageOperator
func applyImageOperator() uintptr {
	return arrayToPtr(buffer)
}

//go:export getInputBuffer
func getInputBuffer(size uint32) uintptr {
	buffer = make([]byte, size)
	return arrayToPtr(buffer)
}

//go:export getOutputBufferSize
func getOutputBufferSize(ptr uintptr) uint32 {
	if arrayToPtr(buffer) == ptr {
		return uint32(len(buffer))
	} else {
		return 0
	}
}

func arrayToPtr(array []byte) uintptr {
	ptr := &array[0]
	return uintptr(unsafe.Pointer(ptr))
}

func main() {}
