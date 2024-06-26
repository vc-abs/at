from core.constants import (
	planetaryFriendships,
	signLords,
)
from core.helpers import (
	getSignDistance,
)


# #NOTE: exaltation and debilitation is not considered for dignity calculation, as its not found in many references.
# #NOTE: Moolatrikona is not used, as it's not used in JH or JA.


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
	dignityIndex = (
		3
		if dispositorName == planet['name']
		else planetaryFriendships[
			(
				planet['name'],
				dispositorName,
			)
		]
		+ getTemporaryRelationshipPoints(
			objects[planet['name']],
			objects[dispositorName],
		)
	) + 2

	dignity = compositeDignities[
		dignityIndex
	]

	return dignity


def getPlanetDignity(chart, planet={}):
	objects = chart.objects
	return getDispositorRelationship(
		planet, objects
	)
