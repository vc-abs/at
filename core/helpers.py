import inspect
from core.constants import objects
from os import path


def isTraditionalObject(object):
	return object['name'] in objects


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
