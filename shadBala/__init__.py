import math
from math import sin, radians
from core.Cached import Cached
from core.constants import (
	planets,
	objectProps,
	degrees,
	kendradiBala,
	signWidth,
	maxPossibleDistance,
)
from core.helpers import (
	getHouseQuality,
	getDistanceInCircle,
	getShortestDistanceInCircle,
)
from core.dignity import (
	getPlanetDignity,
)
from core.varga import getVargaPosition
from core.planetQuality import (
	getPlanetQuality,
)

balaDefaultMaxScore = 60
balaDefaultMinScore = 0
balaDefaultMidScore = (
	balaDefaultMaxScore
	- balaDefaultMinScore
) / 2
distanceToScoreFactor = (
	balaDefaultMaxScore
	/ maxPossibleDistance
)
ucchaBalaScaleFactor = (
	maxPossibleDistance
	/ balaDefaultMaxScore
)


def calculateUcchaBala(planet):
	distanceToExaltation = (
		getShortestDistanceInCircle(
			planet['longitude'],
			objectProps[planet['name']][
				'exaltation'
			],
		)
	)
	distanceToDebilitation = (
		getShortestDistanceInCircle(
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


saptavargajaDignityPoints = {
	'own': 30,
	'greatFriend': 22.5,
	'friend': 15,
	'neutral': 7.5,
	'enemy': 3.75,
	'greatEnemy': 1.875,
}

saptavargajaVargas = [
	1,
	2,
	3,
	9,
	7,
	12,
	30,
]


def calculateSaptavargajaBala(
	planet, chart
):
	total = 0

	for varga in saptavargajaVargas:
		vargaPlanet = getVargaPosition(
			planet, varga
		)

		dignity = getPlanetDignity(
			chart=chart,
			planet=vargaPlanet,
		)

		total += saptavargajaDignityPoints[
			dignity
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


# #FROM: https://sacred-astrology.blogspot.com/2008/03/shadBala-and-its-conceptual-details.html
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
	balas = {
		'ucchaBala': calculateUcchaBala(
			planet
		),
		'saptavargajaBala': calculateSaptavargajaBala(
			planet, chart
		),
		'ojaYugmaBala': calculateOjaYugmaBala(
			planet
		),
		'kendradiBala': calculateKendradiBala(
			planet
		),
		'drekkanaBala': calculateDrekkanaBala(
			planet
		),
	}

	return {
		**balas,
		'sthanaBala': sum(balas.values()),
	}


# #TODO: The results are fairly close to that of JA. There's some difference due to minor differences in the positions of fast moving planets.
def calculateDigBala(planet, chart):
	fullDigBalaHouse = objectProps[
		planet['name']
	]['digBalaHouse']

	fullDigBalaLongitude = (
		chart.objects['asc']['longitude']
		+ (fullDigBalaHouse - 1) * signWidth
	) % degrees

	distance = (
		getShortestDistanceInCircle(
			planet['longitude'],
			fullDigBalaLongitude,
		)
	)

	return (
		maxPossibleDistance - distance
	) * distanceToScoreFactor


def calculateNatonnataBala(
	planet, chart
):
	return (
		balaDefaultMaxScore
		if chart.panchang.tod
		== objectProps[planet['name']][
			'tod'
		]
		else balaDefaultMinScore
	)


def calculatePakshaBala(planet, chart):
	pakshaBalaDirection = (
		1
		if (
			planet['name'] == 'moon'
			or getPlanetQuality(planet, chart)
			!= 'malefic'
		)
		else -1
	)
	objects = chart.objects
	pakshaBalaMultiplier = (
		2 if planet['name'] == 'moon' else 1
	)

	sunMoonDistance = (
		getShortestDistanceInCircle(
			objects['sun']['longitude'],
			objects['moon']['longitude'],
		)
	)
	pakshaBalaValue = (
		sunMoonDistance
		* distanceToScoreFactor
	)

	return (
		balaDefaultMinScore
		+ pakshaBalaValue
		if pakshaBalaDirection > 0
		else balaDefaultMaxScore
		- pakshaBalaValue
	) * pakshaBalaMultiplier


tribaghaPlanetOrder = [
	'mercury',
	'sun',
	'saturn',
	'moon',
	'venus',
	'mars',
]


def calculateTribaghaBala(
	planet, chart
):
	if planet['name'] == 'jupiter':
		return balaDefaultMaxScore

	sunToAscDistance = (
		getDistanceInCircle(
			chart.objects['sun']['longitude'],
			chart.objects['asc']['longitude'],
		)
	)
	tribaghaIndex = int(
		sunToAscDistance // 60
	)

	return (
		balaDefaultMaxScore
		if tribaghaPlanetOrder[
			tribaghaIndex
		]
		== planet['name']
		else balaDefaultMinScore
	)


def calculateAbdaBala(planet):
	return 0


def calculateMaasaBala(planet):
	return 0


def calculateVaaraBala(planet, chart):
	return (
		balaDefaultMaxScore
		if chart.panchang.vaara
		== objectProps[planet['name']][
			'weekday'
		]
		else balaDefaultMinScore
	)


def calculateHoraBala(planet):
	return 0


# #NOTE: The given ayana bala computation is not well understood, despite the availability of few Python resources. The results were verified to be  approximately close to the results from JA for a couple of charts. Conversely the differences between the results might have been due to the differences in planetary longitudes, as seen with the impact on Dig Bala calculations.
declinationTable = [
	0,
	362 / 60.0,
	703 / 60.0,
	1002 / 60.0,
	1238 / 60.0,
	1388 / 60.0,
	1440 / 60.0,
]

obliquity = 23.44  # Current obliquity of the ecliptic in degrees


def calcKranti(longitude):
	sign = (
		-1 if 180 < longitude <= 360 else 1
	)

	if 0 < longitude <= 90:
		bhuja = longitude
	elif 90 < longitude <= 180:
		bhuja = 180.0 - longitude
	elif 180 < longitude <= 270:
		bhuja = longitude - 180
	elif 270 < longitude <= 360:
		bhuja = 360.0 - longitude
	else:
		bhuja = 0.0

	dividend = int(bhuja // 15)
	remainder = bhuja % 15
	remDecl = (
		(
			declinationTable[dividend + 1]
			- declinationTable[dividend]
		)
		* remainder
	) / 15.0

	return (
		declinationTable[dividend] + remDecl
	) * sign + obliquity


def calculateAyanaBala(planet):
	currentAyana = (
		'north'
		if 1 <= planet['sign'] <= 6
		else 'south'
	)
	planetAyana = objectProps[
		planet['name']
	]['ayana']
	ayanaDirection = (
		1
		if (
			planetAyana == 'both'
			or planetAyana == currentAyana
		)
		else -1
	)
	balaMultiplier = (
		2 if planet['name'] == 'sun' else 1
	)

	bala = (
		balaDefaultMidScore
		* (
			1
			+ (
				ayanaDirection
				* calcKranti(
					planet['longitude']
				)
				/ 48
			)
		)
		* balaMultiplier
	)
	print(
		planet['name'],
		planet['longitude'] % signWidth,
		bala,
	)
	return bala


# #NOTE: Yuddha Bala calculation is postponed due to the following reasons. JH doesn't seem to have it. JA has the values from -1 to 1, thus with almost no impact. The information available elsewhere doesn't seem to help much in figuring out the method of calculation.
def calculateYuddhaBala(planet):
	return 0


def calculateKaalaBala(planet, chart):
	balas = {
		'natonnataBala': calculateNatonnataBala(
			planet, chart
		),
		'pakshaBala': calculatePakshaBala(
			planet, chart
		),
		'tribaghaBala': calculateTribaghaBala(
			planet, chart
		),
		'abdaBala': calculateAbdaBala(
			planet
		),
		'maasaBala': calculateMaasaBala(
			planet
		),
		'vaaraBala': calculateVaaraBala(
			planet, chart
		),
		'horaBala': calculateHoraBala(
			planet
		),
		'ayanaBala': calculateAyanaBala(
			planet
		),
		'yuddhaBala': calculateYuddhaBala(
			planet
		),
	}
	return {
		**balas,
		'kaalaBala': sum(balas.values()),
	}


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
	balas = {
		**calculateSthanaBala(
			planet, chart
		),
		'digBala': calculateDigBala(
			planet, chart
		),
		'cheshtaBala': calculateCheshtaBala(
			planet
		),
		'drikBala': calculateDrikBala(
			planet
		),
		'naisargikaBala': calculateNaisargikaBala(
			planet
		),
		**calculateKaalaBala(planet, chart),
	}

	return {
		**balas,
		'shadBala': sum(balas.values()),
	}


def calculateIshtaPhala(shadBala):
	ishtaPhala = (shadBala - 1) / 2
	return ishtaPhala


def calculateKashtaPhala(shadBala):
	kashtaPhala = (shadBala + 1) / 2
	return kashtaPhala


class ShadBala(Cached):
	def __init__(self, chart):
		super().__init__()
		self._chart = chart

	def _getPhalas(self):
		planetPhalas = {}
		for planet in planets:
			shadBala = calculateShadbala(
				self._chart.objects[planet],
				self._chart,
			)
			ishtaPhala = calculateIshtaPhala(
				shadBala['shadBala']
			)
			kashtaPhala = (
				calculateKashtaPhala(
					shadBala['shadBala']
				)
			)
			planetPhalas[planet] = {
				**shadBala,
				'ishtaPhala': ishtaPhala,
				'kashtaPhala': kashtaPhala,
			}

		return planetPhalas
