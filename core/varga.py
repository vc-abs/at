from core.constants import (
	signCount,
	signWidth,
)

specialVargas = {
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
	12: {
		'type': 'sign',
		'offsets': [1],
	},
	24: {},
	30: {},
	40: {},
	45: {},
	60: {},
}

perfectVargas = [9, 16, 20, 27]


def getVargaOffset(
	offsetData, vargaPosition, sign
):
	return (
		offsetData['offsets'][vargaPosition]
		- 1
	)


def getRashiOffset(
	offsetData, vargaPosition, sign
):
	offsets = offsetData['offsets']
	return (
		offsets[(sign - 1) % len(offsets)]
		- 1
		+ vargaPosition
	)


offsetTypeProcessors = {
	'division': getVargaOffset,
	'sign': getRashiOffset,
}


def getOffset(
	varga, vargaPosition, sign
):
	if varga in perfectVargas:
		return 0

	offsetData = specialVargas[varga]
	return offsetTypeProcessors[
		offsetData['type']
	](offsetData, vargaPosition, sign)


def getVargaPosition(planet, varga):
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
		degreesWithinSign * varga
	) % signWidth

	return {
		'sign': vargaSign,
		'degree': vargaDegree,
	}
