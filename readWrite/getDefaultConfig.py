from datetime import (
	datetime,
)

selectAllQuery = 'ilevel_0 in ilevel_0'
defaults = {
	'ayanamsa': 'ay_raman',
	'hour': 0,
	'minute': 0,
	'second': 0,
	# India specific defaults.
	'utcHour': 5,
	'utcMinute': 30,
	# Approximate Location of Mahakaal Jyotirlinga, Ujjain (to align with the many jyotish traditions across India).
	'latitude': 23.101,
	'longitude': 77.461,
	# Records
	'freq': '15min',
	'periods': 700,  # one week approx, when the frequency is 15 mins.
	# Export config.
	'exportSeparator': '\t',
	'query': selectAllQuery,
	'columns': {},
	'order': {},
}


def getDefaultConfig():
	now = datetime.now()

	return {
		**defaults,
		'year': now.year,
		'month': now.month,
		'day': now.day,
	}
