import inspect
import math
from os import path
from core.constants import (
	objects,
	signCount,
	degrees,
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
