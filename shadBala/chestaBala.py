from core.constants import (
	objectProps,
	signWidth,
)

chestaBalaExceptions = {
	'sun': 'ayanaBala',
	'moon': 'pakshaBala',
}

chestaPoints = {
	'vikala': 15,
	'mandatara': 15,
	'manda': 30,
	'sama': 7.5,
	'chara': 45,
	'athiChara': 30,
	'vakra': 60,
	'anuVakra': 30,
}

signChangeWindowInDays = 3


def isSignChanging(planet):
	currentSignIndex = (
		planet['longitude'] % signWidth
	)
	futureSignIndex = (
		planet['longitude']
		+ planet['speed']
		* signChangeWindowInDays
	) % signWidth

	return (
		currentSignIndex != futureSignIndex
	)


def getSpecialPlanetChestaBala(
	planet, kaalaBala
):
	return (
		kaalaBala[
			chestaBalaExceptions[
				planet['name']
			]
		]
		/ 2
	)


def getRetrogradeChestaBala(planet, _):
	if isSignChanging(planet):
		speedClassification = 'vakra'
	else:
		speedClassification = 'anuVakra'

	return chestaPoints[
		speedClassification
	]


def getGeneralChestaBala(planet, _):
	speedIncreasePercent = (
		planet['speed']
		/ objectProps[planet['name']][
			'meanSpeed'
		]
	) * 100

	if speedIncreasePercent < 10:
		speedClassification = 'vikala'
	elif speedIncreasePercent < 50:
		speedClassification = 'mandatara'
	elif speedIncreasePercent < 100:
		speedClassification = 'manda'
	elif speedIncreasePercent < 150:
		speedClassification = 'sama'
	elif isSignChanging(planet):
		speedClassification = 'athiChara'
	else:
		speedClassification = 'chara'

	return chestaPoints[
		speedClassification
	]


chestaCalculators = {
	'special': getSpecialPlanetChestaBala,
	'retro': getRetrogradeChestaBala,
	'general': getGeneralChestaBala,
}


def calculateCheshtaBala(
	planet, kaalaBala
):
	planetName = planet['name']
	chestaCalculatorKey = (
		'special'
		if chestaBalaExceptions.get(
			planetName
		)
		else (
			'retro'
			if planet['retrograde']
			else 'general'
		)
	)

	return chestaCalculators[
		chestaCalculatorKey
	](planet, kaalaBala)
