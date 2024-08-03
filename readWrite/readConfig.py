import hiyapyco
from datetime import (
	datetime,
	timezone,
	timedelta,
)
from readWrite.getDefaultConfig import (
	getDefaultConfig,
)

from os import path

projectRoot = path.realpath(
	path.dirname(__file__) + '/../'
)

eventDefaultKeys = [
	'latitude',
	'longitude',
	'year',
	'month',
	'day',
	'hour',
	'minute',
	'second',
]

defaultEvents = {'default': {}}


def getEventTime(event, config):
	return datetime(
		event['year'],
		event['month'],
		event['day'],
		event['hour'],
		event['minute'],
		event['second'],
		tzinfo=timezone(
			offset=timedelta(
				hours=config['utcHour'],
				minutes=config['utcMinute'],
			)
		),
	)


def buildEvents(config):
	defaultEventConfig = {
		k: config[k]
		for k in eventDefaultKeys
		if k in config
	}
	events = config.get(
		'events', defaultEvents
	)

	extendedEventConfigs = {
		k: {**defaultEventConfig, **event}
		for k, event in events.items()
	}

	return {
		k: {
			**event,
			'date': getEventTime(
				event, config
			),
		}
		for k, event in extendedEventConfigs.items()
	}


def readConfig(filePaths):
	yamlConfig = hiyapyco.load(
		[
			projectRoot
			+ '/data/defaultConfig.yml'
		]
		+ filePaths,
		method=hiyapyco.METHOD_MERGE,
	)
	config = {
		**getDefaultConfig(),
		**yamlConfig,
	}

	return {
		**config,
		'events': buildEvents(config),
	}
