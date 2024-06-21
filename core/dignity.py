from core.constants import (
	planetaryFriendships,
	moolaTrikonaPositions,
	objectProps,
	signLords,
)

# #TODO: Fix the exaltations for Rahu and Ketu, as they are considered to be exalted throughout the rashi.
dignityRangeInDegrees = 2


def isInMoolaTrikona(planet):
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


def getDispositorRelationship(planet):
	# #TODO: Take temporary friendships should be taken into account. This requires house info of the sign lord, thus possibly the entire chart info.
	return (
		2
		if signLords[planet['sign']]
		== planet['name']
		else planetaryFriendships[
			(
				planet['name'],
				signLords[planet['sign']],
			)
		]
	)


dignityClassifiers = {
	'exaltation': lambda planet: abs(
		planet['longitude']
		- objectProps[planet['name']][
			'exaltation'
		]
	)
	< dignityRangeInDegrees,
	'debilitation': lambda planet: abs(
		planet['longitude']
		- objectProps[planet['name']][
			'debilitation'
		]
	)
	< dignityRangeInDegrees,
	'moolatrikona': isInMoolaTrikona,
	'own': lambda planet: getDispositorRelationship(
		planet
	)
	== 2,
	'friend': lambda planet: getDispositorRelationship(
		planet
	)
	== 1,
	'neutral': lambda planet: getDispositorRelationship(
		planet
	)
	== 0,
	'enemy': lambda planet: getDispositorRelationship(
		planet
	)
	== -1,
}


def getPlanetDignity(chart, planet={}):
	for (
		dignity,
		classify,
	) in dignityClassifiers.items():
		if classify(planet):
			return dignity
