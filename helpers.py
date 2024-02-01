from constants import objects

def isTraditionalObject(object):
	return object['name'] in objects

def selectObjects(items, selection=objects):
	return list(filter(lambda item: item['name'] in selection, items))
