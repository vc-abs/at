from np import sign
from at.core.constants import (
	objectProps,
	maxPossibleDistance,
	nodes,
)
from at.core.helpers import (
	getShortestDistanceInCircle,
	getSignDistance,
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


def isAspectingPlanet(basePlanet, influencingPlanet):
	aspectHouses = objectProps[
		influencingPlanet['name']
	].get('aspects', [])
	return getSignDistance(
		influencingPlanet['house'],
		basePlanet['house'],
	) in aspectHouses


def getObjectsAspecting(chart, basePlanet):
	return [
		object
		for object in chart.objects.values()
		if object != basePlanet
		and object['type'] == 'planet'
		and object['name'] not in nodes
		and isAspectingPlanet(
			basePlanet,
			object,
		)
	]


def getMercuryInfluencers(chart):
	mercury = chart.objects['mercury']
	influencers = {
		object['name']: object
		for object in getObjectsConjunctors(
			chart, mercury
		)
	}
	influencers.update(
		{
			object['name']: object
			for object in getObjectsAspecting(
				chart, mercury
			)
		}
	)
	return list(influencers.values())


def getMercuryQuality(chart):
	quality = 0
	for influencer in getMercuryInfluencers(
		chart
	):
		quality += qualityPoints[
			getPlanetQuality(
				influencer, chart
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
