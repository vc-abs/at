from core.constants import (
	signCount,
	signWidth,
)

vargaConfig = {
	3: {
		'type': 'division',
		'offsets': [1, 5, 9],
	},
	4: {
		'type': 'division',
		'offsets': [1, 4, 7, 10],
	},
	5: {
		'type': 'division',
		'offsets': [
			1,
			11,
			9,
			3,
			7,
			2,
			6,
			12,
			10,
			8,
		],
	},
	6: {'type': 'perfect'},
	7: {
		'type': 'sign',
		'offsets': [1, 7],
	},
	8: {'type': 'perfect'},
	9: {'type': 'perfect'},
	10: {
		'type': 'sign',
		'offsets': [1, 9],
	},
	11: {'type': 'perfect'},
	12: {
		'type': 'sign',
		'offsets': [1],
	},
	16: {'type': 'perfect'},
	20: {'type': 'perfect'},
	24: {
		'type': 'sign',
		'offsets': [
			5,
			3,
			3,
			1,
			1,
			11,
			11,
			9,
			9,
			7,
			7,
			5,
		],
	},
	27: {'type': 'perfect'},
	30: {'type': 'custom'},
	40: {
		'type': 'sign',
		'offsets': [
			1,
			6,
			11,
			4,
			9,
			2,
			7,
			12,
			5,
			10,
			3,
			8,
		],
	},
	45: {
		'type': 'sign',
		'offsets': [1, 4, 7, 10],
	},
	60: {
		'type': 'sign',
		'offsets': [1],
	},
}


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
	offsetData = vargaConfig[varga]
	return offsetTypeProcessors[
		offsetData['type']
	](offsetData, vargaPosition, sign)


def getOffsetVargaPosition(
	planet, varga
):
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


def getPerfectVargaPosition(
	planet, varga
):
	vargaLongitude = (
		planet['longitude'] * varga
	)
	vargaDegree = (
		vargaLongitude % signWidth
	)
	vargaSign = (
		int(vargaLongitude // signWidth)
		% signCount
	) + 1

	return {
		'sign': vargaSign,
		'degree': vargaDegree,
	}


def getCustomVargaPosition(
	planet, varga
):
	return 0


vargaTypeProcessors = {
	'perfect': getPerfectVargaPosition,
	'sign': getOffsetVargaPosition,
	'division': getOffsetVargaPosition,
	'custom': getCustomVargaPosition,
}


def getVargaPosition(planet, varga):
	vargaType = vargaConfig.get(
		varga, {}
	).get('type', 'perfect')

	return vargaTypeProcessors[vargaType](
		planet, varga
	)
