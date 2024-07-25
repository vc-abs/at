import datetime
from math import sqrt
from datetime import (
	timezone,
	timedelta,
)
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
from .cheshtaBala import (
	calculateCheshtaBala,
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
	return {
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


natonnataTODValueMaps = {
	'day': {
		'startTime': 'sunrise',
		'endTime': 'sunset',
		'otherTOD': 'night',
	},
	'night': {
		'startTime': 'sunset',
		'endTime': 'nextRise',
		'otherTOD': 'day',
	},
}


def getNatonnataBalaTODValues(chart):
	eventTime = chart.config['datetime']
	riseAndSet = chart.panchang.riseAndSet
	tod = chart.panchang.tod
	natonnataTODValueMap = (
		natonnataTODValueMaps[tod]
	)
	todDuration = (
		riseAndSet[
			natonnataTODValueMap['endTime']
		]
		- riseAndSet[
			natonnataTODValueMap['startTime']
		]
	).total_seconds()
	todElapsed = (
		eventTime
		- riseAndSet[
			natonnataTODValueMap['startTime']
		]
	).total_seconds()

	todBala = balaDefaultMaxScore * (
		1
		- abs(todDuration / 2 - todElapsed)
		/ todDuration
	)

	return {
		'both': balaDefaultMaxScore,
		f'{tod}': todBala,
		f'{natonnataTODValueMap["otherTOD"]}': balaDefaultMaxScore
		- todBala,
	}


def calculateNatonnataBala(
	planet, kaalaValues
):
	return kaalaValues[
		'natonnataBalaTODValues'
	][objectProps[planet['name']]['tod']]


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
	planet, kaalaValues
):
	if planet['name'] == 'jupiter':
		return balaDefaultMaxScore

	tribaghaIndex = int(
		kaalaValues['sunToAscDistance']
		// 60
	)

	return (
		balaDefaultMaxScore
		if tribaghaPlanetOrder[
			tribaghaIndex
		]
		== planet['name']
		else balaDefaultMinScore
	)


indiaTZ = timezone(
	offset=timedelta(
		hours=5,
		minutes=30,
	)
)
aharganaAnchorDate = datetime.datetime(
	2024,
	6,
	17,  # NOTE: Midnight of the previous date.
	tzinfo=indiaTZ,
)


def getAharganaDays(chart):
	eventTime = chart.config['datetime']
	dayOffset = (
		-1
		if chart.panchang.riseAndSet[
			'sunrise'
		]
		> eventTime
		else 0
	)

	return (
		eventTime - aharganaAnchorDate
	).days + dayOffset


bvrAbdaLordOrder = [
	'moon',
	'jupiter',
	'sun',
	'mercury',
	'saturn',
	'mars',
	'venus',
]
abdaLordCount = len(bvrAbdaLordOrder)
bvrAbdaYearLengthInDays = 360
maxAbdaBalaPoints = 15


def calculateAbdaBala(
	planet, kaalaValues
):
	abdaLordIndex = (
		kaalaValues['aharganaDays']
		// bvrAbdaYearLengthInDays
	) % abdaLordCount

	return (
		balaDefaultMinScore
		if planet['name']
		!= bvrAbdaLordOrder[abdaLordIndex]
		else maxAbdaBalaPoints
	)


bvrMaasaLordOrder = [
	'moon',
	'mercury',
	'jupiter',
	'saturn',
	'mars',
	'venus',
	'sun',
]
bvrMaasaLengthInDays = (
	bvrAbdaYearLengthInDays // 12
)
maxMaasaBalaPoints = 30


def calculateMaasaBala(
	planet, kaalaValues
):
	maasaLordIndex = (
		kaalaValues['aharganaDays']
		// bvrMaasaLengthInDays
	) % abdaLordCount

	return (
		balaDefaultMinScore
		if planet['name']
		!= bvrMaasaLordOrder[maasaLordIndex]
		else maxMaasaBalaPoints
	)


maxVaaraBalaPoints = 45


def calculateVaaraBala(
	planet, kaalaValues
):
	return (
		maxVaaraBalaPoints
		if kaalaValues['vaara']
		== objectProps[planet['name']][
			'weekday'
		]
		else balaDefaultMinScore
	)


maxHoraBalaPoints = 60


def calculateHoraBala(
	planet, kaalaValues
):
	return (
		balaDefaultMinScore
		if planet['name']
		!= kaalaValues['hora']
		else maxHoraBalaPoints
	)


# #NOTE: The the given ayana bala computation is somewhat understood, the results seems to be  approximately close to the results from JA for a couple of charts. These may be due to the differences in planetary longitudes, as seen with the impact on Dig Bala calculations. Or some minor issues with computations.
declinationsInDegrees = [
	0,
	362 / 60.0,
	703 / 60.0,
	1002 / 60.0,
	1238 / 60.0,
	1388 / 60.0,
	1440 / 60.0,
]
declinationHouseWidth = 15
maxDeclination = declinationsInDegrees[
	-1
]
equinoxPoint = 180
halfEquinoxPoint = equinoxPoint / 2


def calcDeclination(sayanaLongitude):
	bhuja = halfEquinoxPoint - abs(
		(sayanaLongitude % equinoxPoint)
		- halfEquinoxPoint
	)

	dividend = int(
		bhuja // declinationHouseWidth
	)
	remainder = (
		bhuja % declinationHouseWidth
	)
	remainingDeclination = (
		declinationsInDegrees[dividend + 1]
		- declinationsInDegrees[dividend]
	) * (
		remainder / declinationHouseWidth
	)

	return (
		declinationsInDegrees[dividend]
		+ remainingDeclination
	)


def calculateAyanaBala(
	planet, kaalaValues
):
	ayanamsaOffset = kaalaValues[
		'ayanamsaOffset'
	]
	sayanaLongitude = (
		planet['longitude'] + ayanamsaOffset
	)
	declination = calcDeclination(
		sayanaLongitude
	)

	planetAyana = (
		'north'
		if 0 <= sayanaLongitude < 180
		else 'south'
	)
	beneficialAyanaForPlanet = (
		objectProps[planet['name']]['ayana']
	)
	balaImpactDirection = (
		1
		if (
			beneficialAyanaForPlanet == 'both'
			or beneficialAyanaForPlanet
			== planetAyana
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
			+ balaImpactDirection
			* declination
			/ maxDeclination
		)
	) * balaMultiplier

	return bala


# #NOTE: Yuddha Bala calculation is postponed due to the following reasons. JH doesn't seem to have it. JA has the values from -1 to 1, thus with almost no impact. The information available elsewhere doesn't seem to help much in figuring out the method of calculation.
def calculateYuddhaBala(planet):
	return 0


def calculateKaalaBala(
	planet, chart, context
):
	kaalaValues = context['kaalaValues']

	return {
		'natonnataBala': calculateNatonnataBala(
			planet, kaalaValues
		),
		'pakshaBala': calculatePakshaBala(
			planet, chart
		),
		'tribaghaBala': calculateTribaghaBala(
			planet, kaalaValues
		),
		'abdaBala': calculateAbdaBala(
			planet, kaalaValues
		),
		'maasaBala': calculateMaasaBala(
			planet, kaalaValues
		),
		'vaaraBala': calculateVaaraBala(
			planet, kaalaValues
		),
		'horaBala': calculateHoraBala(
			planet, kaalaValues
		),
		'ayanaBala': calculateAyanaBala(
			planet, kaalaValues
		),
		'yuddhaBala': calculateYuddhaBala(
			planet
		),
	}


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


def calculateShadbala(
	planet, chart, context
):
	sthanaBala = calculateSthanaBala(
		planet, chart
	)
	kaalaBala = calculateKaalaBala(
		planet, chart, context
	)
	otherBalas = {
		'digBala': calculateDigBala(
			planet, chart
		),
		'cheshtaBala': calculateCheshtaBala(
			planet, kaalaBala
		),
		'drikBala': calculateDrikBala(
			planet
		),
		'naisargikaBala': calculateNaisargikaBala(
			planet
		),
	}

	sthanaBalaTotal = sum(
		sthanaBala.values()
	)
	kaalaBalaTotal = sum(
		kaalaBala.values()
	)

	return {
		**sthanaBala,
		'sthanaBala': sthanaBalaTotal,
		**otherBalas,
		**kaalaBala,
		'kaalaBala': kaalaBalaTotal,
		'shadBala': sthanaBalaTotal
		+ kaalaBalaTotal
		+ sum(otherBalas.values()),
	}


def calculateIshtaAndPhalas(shadBala):
	ucchaBala = shadBala['ucchaBala']
	cheshtaBala = shadBala['cheshtaBala']
	return {
		'ishtaPhala': sqrt(
			ucchaBala * cheshtaBala
		),
		'kashtaBala': sqrt(
			(balaDefaultMaxScore - ucchaBala)
			* (
				balaDefaultMaxScore
				- cheshtaBala
			)
		),
	}


def buildContext(chart):
	return {
		'kaalaValues': {
			'ayanamsaOffset': chart.ayanamsa[
				'offset'
			],
			'sunToAscDistance': (
				getDistanceInCircle(
					chart.objects['sun'][
						'longitude'
					],
					chart.objects['asc'][
						'longitude'
					],
				)
			),
			'aharganaDays': getAharganaDays(
				chart
			),
			'vaara': chart.panchang.vaara,
			'hora': chart.panchang.hora,
			'natonnataBalaTODValues': getNatonnataBalaTODValues(
				chart
			),
		}
	}


def calculatePlanetBalas(
	planet, chart, context
):
	shadBala = calculateShadbala(
		chart.objects[planet],
		chart,
		context,
	)
	ishtaAndKashtaPhalas = (
		calculateIshtaAndPhalas(shadBala)
	)
	return {
		**shadBala,
		**ishtaAndKashtaPhalas,
	}


class ShadBala(Cached):
	def __init__(self, chart):
		super().__init__()
		self._chart = chart

	def _getPhalas(self):
		context = buildContext(self._chart)
		return {
			planet: calculatePlanetBalas(
				planet, self._chart, context
			)
			for planet in planets
		}
