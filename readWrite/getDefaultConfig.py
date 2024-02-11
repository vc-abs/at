selectAllQuery = 'ilevel_0 in ilevel_0'
defaults = {
	'ayanamsa': 'ay_raman',
	'hour': 0,
	'minute': 0,
	'second': 0,
	'year': 2024,
	'month': 1,
	'day': 1,
	# India specific defaults.
	'utcHour': 5,
	'utcMinute': 30,
	# Approximate Location of Mahakaal Jyotirlinga, Ujjain (to align with the many jyotish traditions across India).
	'latitude': 23.101,
	'longitude': 77.461,
	# Records
	'freq': '15min',
	'periods': 1000,
	# Export config.
	'exportSeparator': '\t',
	'query': selectAllQuery,
	'columns': {},
	'order': {},
}


def getDefaultConfig():
	return {
		**defaults,
	}
