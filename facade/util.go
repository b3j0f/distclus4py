package main

import (
	"C"
	"distclus/core"
	"testing"

	"golang.org/x/exp/rand"
)

func assertCentroids(elemts []core.Elemt, t *testing.T) {
	if len(elemts) != 2 {
		t.Error("Expected 2 got", len(elemts))
	}
}

func makeElements() []core.Elemt {
	var rgen = rand.New(rand.NewSource(6305689164243))
	var elemts = make([]core.Elemt, 20)
	for i := range elemts {
		var elemt = make([]float64, 2)

		var shift = []float64{2.0, 4.0}
		if i >= 10 {
			shift = []float64{30.0, -15.0}
		}

		for j := range elemt {
			elemt[j] = rgen.Float64() + shift[j]
		}

		elemts[i] = elemt
	}
	return elemts
}

func assertLabels(labels []int, t *testing.T) {
	var label0, label10 int
	for i, label := range labels {
		switch {
		case i == 0:
			label0 = label
		case i < 10:
			if label != label0 {
				t.Error("Expected", label0, "got", label)
			}
		case i == 10:
			label10 = label
			if label10 == label0 {
				t.Error("Expected !=", label0, "got", label)
			}
		default:
			if label != label10 {
				t.Error("Expected", label10, "got", label)
			}
		}
	}
}

func goString(str *C.char) string {
	return C.GoString(str)
}