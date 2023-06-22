package main

import (
	"bytes"
	"image/jpeg"
	"image/png"

	"github.com/extism/go-pdk"
)

//go:export applyImageOperator
func applyImageOperator() int32 {
	img, err := jpeg.Decode(bytes.NewReader(pdk.Input()))
	if err != nil {
		println(err.Error())
		return 0
	}
	resultImage := sobel(img)
	var byteBuffer bytes.Buffer
	png.Encode(&byteBuffer, resultImage)
	mem := pdk.AllocateBytes(byteBuffer.Bytes())

	pdk.OutputMemory(mem)

	return 0
}

func main() {}
