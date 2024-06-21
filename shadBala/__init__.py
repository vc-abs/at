from core.Cached import Cached
from core.constants import (
	planets,
	objectProps,
	degrees,
	kendradiBala,
	signWidth,
	signCount,
)
from core.helpers import (
	getHouseQuality,
	getShortestDistanceInCircle,
)
from core.dignity import (
	getPlanetDignity,
)
from core.varga import getVargaPosition

balaDefaultMaxScore = 60
balaDefaultMinScore = 0
maxDistanceBetweenPoints = degrees / 2
ucchaBalaScaleFactor = (
	maxDistanceBetweenPoints
	/ balaDefaultMaxScore
)


def calculateUcchaBala(planet):
	distanceToExaltation = (
		getShortestDistanceInCircle(
			degrees,
			planet['longitude'],
			objectProps[planet['name']][
				'exaltation'
			],
		)
	)
	distanceToDebilitation = (
		getShortestDistanceInCircle(
			degrees,
			planet['longitude'],
			objectProps[planet['name']][
				'debilitation'
			],
		)
	)

	return (
		balaDefaultMaxScore
		- (
			distanceToExaltation
			/ ucchaBalaScaleFactor
		)
		if (
			distanceToExaltation
			< distanceToDebilitation
		)
		else balaDefaultMinScore
		+ (
			distanceToDebilitation
			/ ucchaBalaScaleFactor
		)
	)


planetDignityPoints = {
	'exaltation': 60,
	'moolatrikona': 45,
	'own': 30,
	'greatFriend': 22.5,
	'friend': 15,
	'neutral': 7.5,
	'enemy': 3.75,
	'greatEnemy': 1.875,
	'debilitation': 0,
}

saptavargajaVargas = [
	1,
	2,
	3,
	7,
	9,
	12,
	30,
]


def calculateSaptavargajaBala(
	planet, chart
):
	# #TODO: The calculated Saptavargaja is different than that in 'Jyotish App'. It looks like it's due to not considering the temporary relationship between planets. Try fixing this.
	# #NOTE: Decided to move with the imprecise calculation for now, as finding the correct methodology might not be feasible, now.
	# #NOTE: There are some minor differences between various software, Ex: between JH and Jyotish App.
	total = 0

	for varga in saptavargajaVargas:
		vargaPosition = getVargaPosition(
			planet, varga
		)
		total += planetDignityPoints[
			getPlanetDignity(
				chart=chart,
				planet={
					**planet,
					**vargaPosition,
				},
			)
		]

	return total


ojaYugmaVargas = [1, 9]


def calculateOjaYugmaForVarga(
	planet, varga
):
	vargaPosition = getVargaPosition(
		planet, varga
	)
	vargaPlanet = {
		**planet,
		**vargaPosition,
	}
	return objectProps[
		vargaPlanet['name']
	]['ojaYugmaBala'][
		1 - (vargaPlanet['sign'] % 2)
	]


def calculateOjaYugmaBala(planet):
	bala = 0

	for varga in ojaYugmaVargas:
		bala += calculateOjaYugmaForVarga(
			planet, varga
		)

	return bala


def calculateKendradiBala(planet):
	return kendradiBala[
		getHouseQuality(planet['house'])
	]


# #FROM: https://sacred-astrology.blogspot.com/2008/03/shadbala-and-its-conceptual-details.html
drekkanaPositions = [
	'male',
	'neutral',
	'female',
]
drekkanaPoints = 15
drekkanaWidth = int(signWidth / 3)


def calculateDrekkanaBala(planet):
	drekkana = int(
		(planet['longitude']) % signWidth
	) // (drekkanaWidth)

	return (
		drekkanaPoints
		if drekkanaPositions[drekkana]
		== objectProps[planet['name']][
			'gender'
		]
		else 0
	)


def calculateSthanaBala(planet, chart):
	return (
		calculateUcchaBala(planet)
		+ calculateSaptavargajaBala(
			planet, chart
		)
		+ calculateOjaYugmaBala(planet)
		+ calculateKendradiBala(planet)
		+ calculateDrekkanaBala(planet)
	)


fullDigBalaPoints = 60
maxPossibleDigBalaDistance = (
	signCount / 2
)


# #TODO: Calculate Dig Bala using distance from ascendant, rather than with houses, for better accuracy.
def calculateDigBala(planet):
	fullDigBalaHouse = objectProps[
		planet['name']
	]['digBalaHouse']

	distance = (
		getShortestDistanceInCircle(
			signCount,
			planet['house'],
			fullDigBalaHouse,
		)
	)

	strength = (
		fullDigBalaPoints
		* (
			maxPossibleDigBalaDistance
			- distance
		)
		/ maxPossibleDigBalaDistance
	)

	return strength


def calculateNatonnataBala(planet):
	return 0


def calculatePakshaBala(planet):
	return 0


def calculateTribaghaBala(planet):
	return 0


def calculateAbdaBala(planet):
	return 0


def calculateMaasaBala(planet):
	return 0


def calculateVaaraBala(planet):
	return 0


def calculateHoraBala(planet):
	return 0


def calculateAyanaBala(planet):
	return 0


def calculateYuddhaBala(planet):
	return 0


def calculateKaalaBala(planet):
	return (
		calculateNatonnataBala(planet)
		+ calculateNatonnataBala(planet)
		+ calculatePakshaBala(planet)
		+ calculateTribaghaBala(planet)
		+ calculateAbdaBala(planet)
		+ calculateMaasaBala(planet)
		+ calculateVaaraBala(planet)
		+ calculateHoraBala(planet)
		+ calculateAyanaBala(planet)
		+ calculateYuddhaBala(planet)
	)


def calculateCheshtaBala(planet):
	# #FIX: Make this calculation precise by taking into account, the planetary speed.
	return (
		balaDefaultMaxScore
		if not planet['retrograde']
		else balaDefaultMinScore
	)


def calculateDrikBala(planet):
	return 0


naisargikaBalaPoints = {
	'sun': 60,
	'moon': 51.43,
	'mars': 17.4,
	'mercury': 25.71,
	'jupiter': 34.29,
	'venus': 42.86,
	'saturn': 8.57,
}


def calculateNaisargikaBala(planet):
	return naisargikaBalaPoints[
		planet['name']
	]


def calculateShadbala(planet, chart):
	return (
		calculateSthanaBala(planet, chart)
		+ calculateDigBala(planet)
		+ calculateKaalaBala(planet)
		+ calculateCheshtaBala(planet)
		+ calculateDrikBala(planet)
		+ calculateNaisargikaBala(planet)
	)


def calculateIshtaPhala(shadbala):
	ishtaPhala = (shadbala - 1) / 2
	return ishtaPhala


def calculateKashtaPhala(shadbala):
	kashtaPhala = (shadbala + 1) / 2
	return kashtaPhala


class ShadBala(Cached):
	def __init__(self, chart):
		super().__init__()
		self._chart = chart

	def _getPhalas(self):
		planetPhalas = {}
		for planet in planets:
			shadbala = calculateShadbala(
				self._chart.objects[planet],
				self._chart,
			)
			ishtaPhala = calculateIshtaPhala(
				shadbala
			)
			kashtaPhala = (
				calculateKashtaPhala(shadbala)
			)
			planetPhalas[planet] = {
				'shadbala': shadbala,
				'ishtaPhala': ishtaPhala,
				'kashtaPhala': kashtaPhala,
			}

		return planetPhalas
