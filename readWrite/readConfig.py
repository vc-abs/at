import hiyapyco
from datetime import (
	datetime,
	timezone,
	timedelta,
)

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
	'freq': '60min',
	'periods': 1000,
	# Export config.
	'exportSeparator': '\t',
	'query': selectAllQuery,
	'columns': {},
	'order': {},
}


def readConfig(filePaths):
	yamlConfig = hiyapyco.load(
		filePaths,
		method=hiyapyco.METHOD_MERGE,
	)
	config = {
		**defaults,
		**yamlConfig,
	}
	config['date'] = datetime(
		config['year'],
		config['month'],
		config['day'],
		config['hour'],
		config['minute'],
		config['second'],
		tzinfo=timezone(
			offset=timedelta(
				hours=config['utcHour'],
				minutes=config['utcMinute'],
			)
		),
	)
	return config
