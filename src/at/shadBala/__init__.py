import datetime
from math import sqrt
from datetime import (
	timezone,
	timedelta,
)
from at.core.Cached import Cached
from at.core.constants import (
	planets,
	objectProps,
	degrees,
	kendradiBala,
	signCount,
	signWidth,
	maxPossibleDistance,
)
from at.core.helpers import (
	getHouseQuality,
	getDistanceInCircle,
	getShortestDistanceInCircle,
)
from at.core.dignity import (
	getPlanetDignity,
)
from at.core.varga import getVargaPosition
from at.core.planetQuality import (
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


# #NOTE: BPHS-oriented Dig Bala is treated here as a linear falloff from the
# directional-strength house longitude to the opposite point. JA comparisons
# remain manual reference checks outside this implementation.
def getDigBalaReferenceLongitude(planet, chart):
	fullDigBalaHouse = objectProps[
		planet['name']
	]['digBalaHouse']

	return (
		chart.objects['asc']['longitude']
		+ (fullDigBalaHouse - 1) * signWidth
	) % degrees



def calculateDigBala(planet, chart):
	distance = getShortestDistanceInCircle(
		planet['longitude'],
		getDigBalaReferenceLongitude(
			planet, chart
		),
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


tribaghaBalaPointsByPlanet = {
	'jupiter': balaDefaultMaxScore,
}


def calculateTribaghaBala(
	planet, kaalaValues
):
	planetName = planet['name']
	if planetName in tribaghaBalaPointsByPlanet:
		return tribaghaBalaPointsByPlanet[
			planetName
		]

	tribaghaIndex = int(
		kaalaValues['sunToAscDistance']
		// 60
	)

	return (
		balaDefaultMaxScore
		if tribaghaPlanetOrder[
			tribaghaIndex
		]
		== planetName
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


def getAbdaLordIndex(kaalaValues):
	return (
		kaalaValues['aharganaDays']
		// bvrAbdaYearLengthInDays
	) % abdaLordCount



def calculateAbdaBala(
	planet, kaalaValues
):
	abdaLordIndex = getAbdaLordIndex(
		kaalaValues
	)

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


def getMaasaLordIndex(kaalaValues):
	return (
		kaalaValues['aharganaDays']
		// bvrMaasaLengthInDays
	) % abdaLordCount



def calculateMaasaBala(
	planet, kaalaValues
):
	maasaLordIndex = getMaasaLordIndex(
		kaalaValues
	)

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


# #NOTE: Ayana Bala follows a BPHS-oriented kranti-based formula here,
# using signed declination from sayana longitude and the standard planet
# groupings reflected in the companion `src/at/shadBala/.ayana.py` sketch.
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
	if dividend >= len(declinationsInDegrees) - 1:
		return declinationsInDegrees[-1]

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


def calculateKranti(sayanaLongitude):
	declination = calcDeclination(
		sayanaLongitude
	)
	return (
		declination
		if 0 <= (sayanaLongitude % 360) < equinoxPoint
		else -declination
	)


ayanaBalaKrantiAdjustments = {
	'sun': lambda kranti: 24 + kranti,
	'venus': lambda kranti: 24 + kranti,
	'mars': lambda kranti: 24 + kranti,
	'jupiter': lambda kranti: 24 + kranti,
	'moon': lambda kranti: 24 - kranti,
	'saturn': lambda kranti: 24 - kranti,
	'mercury': lambda kranti: 24 + abs(kranti),
}

ayanaBalaMultipliers = {
	'sun': 2,
	'moon': 1,
	'mars': 1,
	'mercury': 1,
	'jupiter': 1,
	'venus': 1,
	'saturn': 1,
}


def calculateAyanaBala(
	planet, kaalaValues
):
	ayanamsaOffset = kaalaValues[
		'ayanamsaOffset'
	]
	sayanaLongitude = (
		planet['longitude'] + ayanamsaOffset
	)
	kranti = calculateKranti(
		sayanaLongitude
	)
	planetName = planet['name']
	baseBala = (
		ayanaBalaKrantiAdjustments[planetName](
			kranti
		)
		* 60
	) / 48

	return (
		baseBala
		* ayanaBalaMultipliers[planetName]
	)


planetDiscDiameters = {
	'mars': 9.4,
	'mercury': 6.6,
	'jupiter': 190.4,
	'venus': 16.6,
	'saturn': 158.0,
}

yuddhaBalaRelevantKaalaKeys = {
	'natonnataBala',
	'pakshaBala',
	'tribaghaBala',
	'horaBala',
}


def getYuddhaBalaCandidates(chart):
	candidates = [
		chart.objects[planet]
		for planet in planets
		if (
			planet not in {'sun', 'moon'}
			and planet in chart.objects
		)
	]
	closestPair = None
	closestDistance = None

	for index, left in enumerate(candidates):
		for right in candidates[index + 1 :]:
			distance = getShortestDistanceInCircle(
				left['longitude'],
				right['longitude'],
				degrees,
			)
			if closestDistance is None or distance < closestDistance:
				closestDistance = distance
				closestPair = (left, right)

	return closestPair, closestDistance



def getYuddhaBalaBaseTotals(chart, context, planetsInWar):
	baseTotals = {}
	for planet in planetsInWar:
		kaalaBala = {
			'natonnataBala': calculateNatonnataBala(
				planet, context['kaalaValues']
			),
			'pakshaBala': calculatePakshaBala(
				planet, chart
			),
			'tribaghaBala': calculateTribaghaBala(
				planet, context['kaalaValues']
			),
			'horaBala': calculateHoraBala(
				planet, context['kaalaValues']
			),
		}
		baseTotals[planet['name']] = (
			sum(
				calculateSthanaBala(
					planet, chart
				).values()
			)
			+ calculateDigBala(
				planet, chart
			)
			+ sum(
				kaalaBala[key]
				for key in yuddhaBalaRelevantKaalaKeys
			)
		)
	return baseTotals



def calculateYuddhaBala(planet, chart, context):
	planetsInWar, closestDistance = getYuddhaBalaCandidates(
		chart
	)
	if (
		planetsInWar is None
		or planet['name'] not in {
			planetsInWar[0]['name'],
			planetsInWar[1]['name'],
		}
	):
		return 0

	baseTotals = getYuddhaBalaBaseTotals(
		chart,
		context,
		planetsInWar,
	)
	left, right = planetsInWar
	baseDifference = abs(
		baseTotals[left['name']]
		- baseTotals[right['name']]
	)
	diameterDifference = abs(
		planetDiscDiameters[left['name']]
		- planetDiscDiameters[right['name']]
	)
	yuddhaBala = (
		0
		if diameterDifference == 0
		else round(
			baseDifference / diameterDifference,
			2,
		)
	)

	if planet['name'] == left['name']:
		return yuddhaBala
	return -yuddhaBala


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
			planet,
			chart,
			context,
		),
	}


drikBalaBenefics = {'moon', 'mercury', 'jupiter', 'venus'}
drikBalaMalefics = {'sun', 'mars', 'saturn'}


def calculateDrikAspectStrength(aspectingPlanet, targetPlanet):
	distance = getDistanceInCircle(
		aspectingPlanet['longitude'],
		targetPlanet['longitude'],
		degrees,
	)
	planetName = aspectingPlanet['name']
	strength = 0.0

	if 30.01 <= distance <= 60.0:
		strength = 0.5 * (distance - 30.0)
	elif 60.01 <= distance <= 90.0:
		strength = (distance - 60.0) + 15
		if planetName == 'saturn':
			strength += 45
	elif 90.01 <= distance <= 120.0:
		strength = 0.5 * (120.0 - distance) + 30
		if planetName == 'mars':
			strength += 15
	elif 120.01 <= distance <= 150.0:
		strength = 150.0 - distance
		if planetName == 'jupiter':
			strength += 30
	elif 150.01 <= distance <= 180.0:
		strength = 2.0 * (distance - 150.0)
	elif 180.01 <= distance <= 300.0:
		strength = 0.5 * (300.0 - distance)
		if planetName == 'mars' and 210.01 < distance < 240.01:
			strength += 15
		if planetName == 'jupiter' and 240.01 < distance < 270.01:
			strength += 30
		if planetName == 'saturn' and 270.01 < distance < 300.01:
			strength += 45

	return round(strength * 0.25, 2)



def getDrikBalaAspectContributions(planet, chart):
	contributions = []
	for source in chart.objects.values():
		if (
			source == planet
			or source.get('type') != 'planet'
			or source['name'] not in planets
		):
			continue

		aspectHouses = objectProps[
			source['name']
		].get('aspects', [])
		if getDistanceInCircle(
			source['house'],
			planet['house'],
			signCount,
		) not in aspectHouses:
			continue

		strength = calculateDrikAspectStrength(
			source,
			planet,
		)
		if source['name'] in drikBalaBenefics:
			contributions.append(strength)
		elif source['name'] in drikBalaMalefics:
			contributions.append(-strength)

	return contributions



def calculateDrikBala(planet, chart):
	return round(
		sum(
			getDrikBalaAspectContributions(
				planet, chart
			)
		) / 4,
		2,
	)


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
			planet, chart
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


def calculatePhalas(shadBala):
	ucchaBala = shadBala['ucchaBala']
	cheshtaBala = shadBala['cheshtaBala']
	return {
		'ishtaPhala': sqrt(
			ucchaBala * cheshtaBala
		),
		'kashtaPhala': sqrt(
			(balaDefaultMaxScore - ucchaBala)
			* (
				balaDefaultMaxScore
				- cheshtaBala
			)
		),
	}


shadBalaMedianStrengths = {
	'sun': 300,
	'moon': 360,
	'mars': 300,
	'mercury': 420,
	'jupiter': 390,
	'venus': 330,
	'saturn': 300,
}


def calculateStrength(planet, shadBala):
	return {
		'strength': shadBala['shadBala']
		/ shadBalaMedianStrengths[planet]
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

	return {
		**shadBala,
		**calculateStrength(
			planet, shadBala
		),
		**calculatePhalas(shadBala),
	}


class ShadBala(Cached):
	def __init__(self, chart):
		super().__init__()
		self._chart = chart

	def _getBalas(self):
		context = buildContext(self._chart)
		return {
			planet: calculatePlanetBalas(
				planet, self._chart, context
			)
			for planet in planets
		}
