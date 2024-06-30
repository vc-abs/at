from np import sign
from core.constants import (
	objectProps,
	maxPossibleDistance,
)
from core.helpers import (
	getShortestDistanceInCircle,
)

planetQualities = [
	'malefic',
	'neutral',
	'benefic',
]

qualityPoints = {
	'malefic': -1,
	'benefic': 1,
}


def getObjectsConjunctors(
	chart, basePlanet
):
	house = basePlanet['house']

	return [
		object
		for object in chart.objects.values()
		if object != basePlanet
		and object['house'] == house
		and object['type'] == 'planet'
	]


# #TODO: Improve the quality finding logic of mercury by considering planetary aspects.
def getMercuryQuality(chart):
	quality = 0
	conjunctors = getObjectsConjunctors(
		chart, chart.objects['mercury']
	)

	for conjunctor in conjunctors:
		quality += qualityPoints[
			getPlanetQuality(
				conjunctor, chart
			)
		]
	return sign(quality)


conditionalQualifiers = {
	# #NOTE: There could be a minor discrepancy with JA in calculating the quality of the moon, as it depends upon tithis and below it depends upon degrees.
	'moon': lambda chart: 1
	if getShortestDistanceInCircle(
		chart.objects['sun']['longitude'],
		chart.objects['moon']['longitude'],
	)
	> maxPossibleDistance / 2
	else -1,
	'mercury': getMercuryQuality,
}


def getPlanetQuality(planet, chart):
	planetName = planet['name']
	planetQuality = objectProps[
		planetName
	]['quality']
	return (
		planetQuality
		if planetQuality != 'conditional'
		else planetQualities[
			conditionalQualifiers[planetName](
				chart
			)
			+ 1
		]
	)
