from np import sign
from at.core.constants import (
	objectProps,
	nodes,
	tithiCount,
)
from at.core.helpers import getSignDistance

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
	return int(sign(quality))


moonBeneficTithiStart = 8
moonBeneficTithiEnd = 23
moonFullnessMidpoint = 15.5
moonMaxCircularTithiDistance = tithiCount / 2


def normalizeMoonTithi(tithi):
	return tithiCount if tithi == 0 else tithi


def getMoonQualityScore(chart):
	tithi = normalizeMoonTithi(
		chart.panchang.tithi
	)
	distanceFromFullMoon = min(
		abs(tithi - moonFullnessMidpoint),
		tithiCount - abs(tithi - moonFullnessMidpoint),
	)
	score = (
		moonBeneficTithiStart
		- distanceFromFullMoon
	)
	return score


def getMoonQuality(chart):
	return int(
		sign(
			getMoonQualityScore(chart)
		)
	)


conditionalQualifiers = {
	'moon': getMoonQuality,
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
