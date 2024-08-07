import yaml
from deepmerge import Merger
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

merger = Merger(
    [
        (dict, ["merge"])
    ],
    ["override"],
    ["override"]
)

def mergeFiles(filePaths):
    data = [yaml.safe_load(open(file, 'r')) for file in filePaths]
    mergedData = data[0]
    for d in data[1:]:
        mergedData = merger.merge(mergedData, d)
    return mergedData

def readConfig(filePaths):
	yamlFiles = [
			projectRoot
			+ '/data/defaultConfig.yml'
		] + filePaths
	mergedYML = mergeFiles(yamlFiles)

	config = {
		**getDefaultConfig(),
		**mergedYML,
	}

	return {
		**config,
		'events': buildEvents(config),
	}
