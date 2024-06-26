from core.constants import (
	objectProps,
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


specialPositionClassifiers = {
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
}


def getPlanetSpecialPosition(planet):
	for (
		specialPosition,
		classify,
	) in (
		specialPositionClassifiers.items()
	):
		if classify(planet):
			return specialPosition
