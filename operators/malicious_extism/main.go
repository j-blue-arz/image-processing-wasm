package main

import (
	"github.com/extism/go-pdk"
)

//go:export applyImageOperator
func applyImageOperator() int32 {
	pdk.Log(pdk.LogDebug, "debug-log")

	req := pdk.NewHTTPRequest("GET", "https://www.random.org/integers/?num=1&min=1&max=1000&format=plain&col=1&base=10")
	res := req.Send()

	pdk.OutputMemory(res.Memory())

	return 0
}

func main() {}
