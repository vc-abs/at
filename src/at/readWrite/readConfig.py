import yaml
from deepmerge import Merger
from datetime import (
	datetime,
	timezone,
	timedelta,
)
from at.readWrite.getDefaultConfig import (
	getDefaultConfig,
)

from os import path

projectRoot = path.realpath(
	path.dirname(__file__) + '/../../..'
)

scenarioDefaultKeys = [
	'latitude',
	'longitude',
	'year',
	'month',
	'day',
	'hour',
	'minute',
	'second',
]

defaultScenarios = {'default': {}}


def getScenarioTime(scenario, config):
	return datetime(
		scenario['year'],
		scenario['month'],
		scenario['day'],
		scenario['hour'],
		scenario['minute'],
		scenario['second'],
		tzinfo=timezone(
			offset=timedelta(
				hours=config['utcHour'],
				minutes=config['utcMinute'],
			)
		),
	)


def buildScenarios(config):
	defaultScenarioConfig = {
		k: config[k]
		for k in scenarioDefaultKeys
		if k in config
	}
	scenarios = config.get(
		'scenarios', defaultScenarios
	)

	extendedScenarioConfigs = {
		k: {**defaultScenarioConfig, **scenario}
		for k, scenario in scenarios.items()
	}

	return {
		k: {
			**scenario,
			'date': getScenarioTime(
				scenario, config
			),
		}
		for k, scenario in extendedScenarioConfigs.items()
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
		'scenarios': buildScenarios(config),
	}
