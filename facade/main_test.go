package main

import (
	"testing"
)

func TestRegisterAlgorithm(t *testing.T) {
	var descr0 = makeAlgorithm()
	var descr1 = makeAlgorithm()

	if descr1 <= descr0 {
		t.Error("Expected greate than descr0 got", descr1)
	}

	UnregisterAlgorithm(descr0)
	UnregisterAlgorithm(descr1)
}

func TestGetAlgorithm(t *testing.T) {
	var descr0 = makeAlgorithm()
	var descr1 = makeAlgorithm()

	var algo0 = GetAlgorithm(descr0)

	if algo0 == nil {
		t.Error("Expected pointer got nil")
	}

	var algo1 = GetAlgorithm(descr1)

	if algo1 == nil {
		t.Error("Expected pointer got nil")
	}

	if algo0 == algo1 {
		t.Error("Expect distinct pointers got same")
	}

	UnregisterAlgorithm(descr0)
	UnregisterAlgorithm(descr1)
}

func TestUnregisterAlgorithm(t *testing.T) {
	var descr0 = makeAlgorithm()
	UnregisterAlgorithm(descr0)

	var algo0 = GetAlgorithm(descr0)

	if algo0 != nil {
		t.Error("Expected nil got pointer")
	}
}

func makeAlgorithm() AlgorithmDescr {
	var elemts = makeElements()
	var arr, l1, l2 = RealElemtsToArray(elemts)
	return (int)(MCMC(
		0, 0, 0, 6305689164243,
		arr, l1, l2,
		2, 2, 3, 30, 100,
		100.0, 1.0, 2.0, 1.0,
		1,
		0, 0,
	))
}
