import hiyapyco
from datetime import (
	datetime,
	timezone,
	timedelta,
)
from readWrite.getDefaultConfig import (
	getDefaultConfig,
)


def readConfig(filePaths):
	yamlConfig = hiyapyco.load(
		filePaths,
		method=hiyapyco.METHOD_MERGE,
	)
	config = {
		**getDefaultConfig(),
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
