package main

import (
	"bytes"
	"image/jpeg"

	"github.com/extism/go-pdk"
)

//go:export applyImageOperator
func applyImageOperator() int32 {
	inputBytes := pdk.Input()

	result := applyOperatorOnJpeg(inputBytes)

	mem := pdk.AllocateBytes(result.Bytes())
	pdk.OutputMemory(mem)

	return 0
}

func applyOperatorOnJpeg(input []byte) bytes.Buffer {
	img, err := jpeg.Decode(bytes.NewReader(input))
	if err != nil {
		println(err.Error())
	}
	resultImage := sobel(img)
	var byteBuffer bytes.Buffer
	jpeg.Encode(&byteBuffer, resultImage, nil)
	return byteBuffer
}

func main() {}
