from core.constants import (
	planetaryFriendships,
	moolaTrikonaPositions,
	objectProps,
	signLords,
)
from core.helpers import (
	getHouseDistance,
)

# #TODO: Fix the exaltations for Rahu and Ketu, as they are considered to be exalted throughout the rashi.
dignityRangeInDegrees = 2


def isInMoolaTrikona(planet, *_):
	moolaTrikonaRange = (
		moolaTrikonaPositions.get(
			planet['name'],
			{'start': 0, 'end': 0},
		)
	)

	return (
		moolaTrikonaRange['start']
		<= planet['longitude']
		< moolaTrikonaRange['end']
	)


def getTemporaryRelationshipPoints(
	planet, dispositor
):
	houseDistance = getHouseDistance(
		planet, dispositor
	)
	return (
		1
		if 9 > houseDistance
		or houseDistance < 5
		else -1
	)


def getDispositorRelationship(
	planet, objects
):
	dispositorName = signLords[
		planet['sign']
	]
	dispositor = objects[dispositorName]
	return (
		3
		if dispositorName == planet['name']
		else planetaryFriendships[
			(
				planet['name'],
				signLords[planet['sign']],
			)
		]
		+ getTemporaryRelationshipPoints(
			planet, dispositor
		)
	)


dignityClassifiers = {
	'exaltation': lambda planet, *_: abs(
		planet['longitude']
		- objectProps[planet['name']][
			'exaltation'
		]
	)
	< dignityRangeInDegrees,
	'debilitation': lambda planet,
	*_: abs(
		planet['longitude']
		- objectProps[planet['name']][
			'debilitation'
		]
	)
	< dignityRangeInDegrees,
	'moolatrikona': isInMoolaTrikona,
	'own': lambda planet,
	dispositorRelationship: dispositorRelationship
	== 3,
	# #TODO: Use lists to improve the efficiency of dignity calculations.
	'greatFriend': lambda planet,
	dispositorRelationship: dispositorRelationship
	== 2,
	'friend': lambda planet,
	dispositorRelationship: dispositorRelationship
	== 1,
	'neutral': lambda planet,
	dispositorRelationship: dispositorRelationship
	== 0,
	'enemy': lambda planet,
	dispositorRelationship: dispositorRelationship
	== -1,
	'greatEnemy': lambda planet,
	dispositorRelationship: dispositorRelationship
	== -2,
}


def getPlanetDignity(chart, planet={}):
	dispositorRelationship = (
		getDispositorRelationship(
			planet, chart.objects
		)
	)
	for (
		dignity,
		classify,
	) in dignityClassifiers.items():
		if classify(
			planet, dispositorRelationship
		):
			return dignity
