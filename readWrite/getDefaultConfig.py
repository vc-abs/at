from datetime import (
	datetime,
)

selectAllQuery = 'ilevel_0 in ilevel_0'


def getDefaultConfig():
	now = datetime.now()

	return {
		'year': now.year,
		'month': now.month,
		'day': now.day,
		'hour': now.hour,
		'minute': now.minute,
		'second': now.second,
		'query': selectAllQuery,
		'fieldSets': {},
		'customColumns': {},
		'skipColumns': [],
		'order': {},
	}
