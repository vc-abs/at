import inspect
import math
from os import path
from core.constants import (
	objects,
	signCount,
	degrees,
	objectProps,
	houseQualities,
)


def isTraditionalObject(object):
	return object['name'] in objects


def getOrdinalPosition(
	cardinalPosition,
	segmentCount=signCount,
):
	return math.ceil(
		cardinalPosition
		/ (degrees / segmentCount)
	)


def selectObjects(
	items, selection=objects
):
	return list(
		filter(
			lambda item: item['name']
			in selection,
			items,
		)
	)


def fold(listOfDicts, prop='name'):
	return {
		item[prop]: item
		for item in listOfDicts
	}


def select(dict, keys):
	return {
		key: dict[key] for key in keys
	}


def resolveRelativePath(leaf):
	return path.join(
		path.dirname(
			inspect.stack()[1].filename
		),
		leaf,
	)


def getPlanetaryQuality(planet):
	return objectProps[planet['name']][
		'quality'
	]


def getHouseQuality(house):
	return houseQualities[(house + 2) % 3]


def getShortestDistanceInCircle(
	circumference, p1Distance, p2Distance
):
	return min(
		(
			circumference
			+ p1Distance
			- p2Distance
		)
		% circumference,
		(
			circumference
			+ p2Distance
			- p1Distance
		)
		% circumference,
	)


def getHouseDistance(
	fromObject, toObject
):
	fromHouse = fromObject['house']
	toHouse = toObject['house']
	return (
		abs(toHouse + signCount - fromHouse)
	) % (signCount) + (
		1 if toHouse <= fromHouse else 0
	)
