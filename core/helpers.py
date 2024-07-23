import inspect
import math
from os import path
from core.constants import (
	objects,
	signCount,
	signWidth,
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


def normalizeCircularValue(
	value, circumference
):
	return (
		value + circumference - 1
	) % circumference + 1


def getDistanceInCircle(
	p1DistanceFromStart,
	p2DistanceFromStart,
	circumference=degrees,
):
	return (
		circumference
		+ p2DistanceFromStart
		- p1DistanceFromStart
	) % circumference


def getShortestDistanceInCircle(
	p1DistanceFromStart,
	p2DistanceFromStart,
	circumference=degrees,
):
	return min(
		getDistanceInCircle(
			p1DistanceFromStart,
			p2DistanceFromStart,
			circumference,
		),
		getDistanceInCircle(
			p2DistanceFromStart,
			p1DistanceFromStart,
			circumference,
		),
	)


def getSignDistance(fromSign, toSign):
	return (
		abs(toSign + signCount - fromSign)
	) % signCount + 1


def getSignFromLongitude(longitude):
	return int(longitude / signWidth) + 1
