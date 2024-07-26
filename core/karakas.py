from core.constants import (
	dayRulers,
	signWidth,
)

karakaOrder = [
	'ak',
	'amk',
	'bk',
	'mk',
	'pk',
	'gk',
	'dk',
]


def sortByDegree(object):
	return signWidth - (
		object['longitude'] % signWidth
	)


def getKarakas(chart):
	filteredObjects = [
		object
		for object in chart.objects.values()
		if object['name'] in dayRulers
	]
	sortedObjects = sorted(
		filteredObjects, key=sortByDegree
	)

	planetNames = [
		planet['name']
		for planet in sortedObjects
	]

	return {
		karakatva: planetName
		for karakatva, planetName in zip(
			karakaOrder, planetNames
		)
	}
