from core.constants import (
	signCount,
	signWidth,
)

vargaOffsets = {
	3: {
		'type': 'division',
		'offsets': [1, 5, 9],
	},
	4: {
		'type': 'division',
		'offsets': [1, 4, 7, 10],
	},
	7: {
		'type': 'sign',
		'offsets': [1, 7],
	},
	10: {
		'type': 'sign',
		'offsets': [1, 9],
	},
}


def getDivisionOffset(
	offsetData, vargaPosition, sign
):
	return (
		offsetData['offsets'][vargaPosition]
		- 1
	)


def getSignOffset(
	offsetData, vargaPosition, sign
):
	offsets = offsetData['offsets']
	return (
		offsets[(sign - 1) % len(offsets)]
		- 1
		+ vargaPosition
	)


offsetTypeProcessors = {
	'division': getDivisionOffset,
	'sign': getSignOffset,
}


def getOffset(
	varga, vargaPosition, sign
):
	offsetData = vargaOffsets[varga]
	return offsetTypeProcessors[
		offsetData['type']
	](offsetData, vargaPosition, sign)


def getVarga(planet, varga):
	longitude = planet['longitude']
	signIndex = planet['sign'] - 1
	degreesWithinSign = (
		longitude % signWidth
	)
	vargaWidth = signWidth / varga
	vargaPosition = int(
		degreesWithinSign // vargaWidth
	)
	offset = getOffset(
		varga, vargaPosition, planet['sign']
	)

	vargaSign = int(
		(signIndex + offset) % signCount + 1
	)
	vargaDegree = (
		degreesWithinSign
		* varga
		% signWidth
	)

	return {
		'sign': vargaSign,
		'degree': vargaDegree,
	}
