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
		'query': selectAllQuery,
		'columns': {},
		'order': {},
	}
