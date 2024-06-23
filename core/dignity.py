from core.constants import (
	planetaryFriendships,
	objectProps,
	signLords,
)
from core.helpers import (
	getSignDistance,
)

# #TODO: Fix the exaltations for Rahu and Ketu, as they are considered to be exalted throughout the rashi.
dignityRangeInDegrees = 2


def isInMoolaTrikona(planet, *_):
	moolaTrikonaStart, moolaTrikonaEnd = (
		objectProps[planet['name']].get(
			'moolaTrikona',
			[0, 0],
		)
	)

	return (
		moolaTrikonaStart
		<= planet['longitude']
		< moolaTrikonaEnd
	)


def getTemporaryRelationshipPoints(
	planet, dispositor
):
	signDistance = getSignDistance(
		planet['sign'], dispositor['sign']
	)

	return (
		1
		if (
			1 < signDistance < 5
			or 9 < signDistance
		)
		else -1
	)


compositeDignities = [
	'greatEnemy',
	'enemy',
	'neutral',
	'friend',
	'greatFriend',
	'own',
]


def getDispositorRelationship(
	planet, objects
):
	dispositorName = signLords[
		planet['sign']
	]
	dispositor = objects[dispositorName]
	dignityIndex = (
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
	) + 2

	dignity = compositeDignities[
		dignityIndex
	]

	return dignity


dignityClassifiers = {
	# #NOTE: exaltation and debilitation is not considered as its not found in many references.
	'moolatrikona': isInMoolaTrikona,
}


def getPlanetDignity(
	objects, planet={}
):
	for (
		dignity,
		classify,
	) in dignityClassifiers.items():
		if classify(planet):
			return dignity

	return getDispositorRelationship(
		planet, objects
	)
