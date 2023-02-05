package main

import (
	"os"
	"unsafe"
)

var buffer []byte

//go:export applyImageOperator
func applyImageOperator() uintptr {
	content := []byte("u got pwn3d\n")
	err := os.WriteFile("virus.txt", content, 0644)
	if err != nil {
		println(err.Error())
		panic(err)
	}
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
