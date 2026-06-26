import re
from os import path
from datetime import (
	datetime,
	timezone,
	timedelta,
)

import yaml
import pandas as pd
from deepmerge import Merger

from at.readWrite.getDefaultConfig import (
	getDefaultConfig,
)

projectRoot = path.realpath(
	path.dirname(__file__) + '/../../..'
)

_DMS_COMPACT_RE = re.compile(
	r'^(?P<deg>\d+)(?P<hemi>[NSEW])(?P<min>\d{2})(?P<sec>\d{2})?$'
)

defaultScenarios = {'default': {}}


def _parseDateString(dateStr):
	parts = str(dateStr).split('-')
	if len(parts) != 3:
		raise ValueError(f'Invalid date format: {dateStr} (expected (YY)YY-MM-DD)')
	yearStr, monthStr, dayStr = parts
	year = int(yearStr)
	if len(yearStr) == 2:
		year = 2000 + year
	elif len(yearStr) != 4:
		raise ValueError(f'Invalid year width in date: {dateStr}')
	return year, int(monthStr), int(dayStr)


def _parseTimeString(timeStr):
	parts = str(timeStr).split(':')
	if len(parts) != 3:
		raise ValueError(f'Invalid time format: {timeStr} (expected hh:mm:ss)')
	hour, minute, second = map(int, parts)
	return hour, minute, second


def _parseDMSValue(value):
	if isinstance(value, (int, float)):
		return float(value)

	v = str(value).strip()
	if not v:
		raise ValueError('Empty coordinate string is invalid')

	m = _DMS_COMPACT_RE.match(v)
	if m:
		sign = -1 if m.group('hemi') in ('S', 'W') else 1
		return sign * (
			int(m.group('deg'))
			+ int(m.group('min')) / 60
			+ int(m.group('sec') or '0') / 3600
		)

	try:
		return float(v)
	except ValueError as exc:
		raise ValueError(f'Invalid coordinate encoding: {value}') from exc


def _utcOffset(config):
	return timezone(
		offset=timedelta(
			hours=config['utcHour'],
			minutes=config['utcMinute'],
		)
	)


def getScenarioTime(scenario, config):
	return datetime(
		scenario['year'], scenario['month'], scenario['day'],
		scenario['hour'], scenario['minute'], scenario['second'],
		tzinfo=_utcOffset(config),
	)


def _standardizeConfig(config):
	for key in ('latitude', 'longitude'):
		if key in config:
			config[key] = _parseDMSValue(config[key])

	if 'startDate' in config:
		config['year'], config['month'], config['day'] = _parseDateString(config.pop('startDate'))
	if 'startTime' in config:
		config['hour'], config['minute'], config['second'] = _parseTimeString(config.pop('startTime'))

	if ('endDate' in config) ^ ('endTime' in config):
		raise ValueError('If specifying endDate you must also specify endTime (and vice-versa).')

	if 'frequency' in config:
		config['interval'] = config.pop('frequency')
	if 'periods' in config:
		config['count'] = config.pop('periods')

	if 'interval' not in config:
		raise ValueError('interval is required.')

	offset = pd.tseries.frequencies.to_offset(config['interval'])
	if not isinstance(offset, pd.offsets.Tick):
		raise ValueError(
			f'interval must be a fixed duration (e.g. 1h, 15min, 1d): {config["interval"]}'
		)

	start = getScenarioTime(config, config)
	config['date'] = start

	if 'endDate' in config and 'endTime' in config:
		year, month, day = _parseDateString(config['endDate'])
		hour, minute, second = _parseTimeString(config['endTime'])
		end = datetime(year, month, day, hour, minute, second, tzinfo=_utcOffset(config))
		config['count'] = len(pd.date_range(
			start=start, end=end, freq=config['interval'], inclusive='both',
		))
	elif 'count' not in config:
		raise ValueError('count is required when endDate/endTime is not provided.')

	return config


def buildScenarios(config):
	scenarios = config.get('scenarios', defaultScenarios)
	return {
		k: _standardizeConfig({**config, **scenario})
		for k, scenario in scenarios.items()
	}


merger = Merger(
	[(dict, ['merge'])],
	['override'],
	['override'],
)


def mergeFiles(filePaths):
	data = [yaml.safe_load(open(file, 'r')) for file in filePaths]
	mergedData = data[0]
	for d in data[1:]:
		mergedData = merger.merge(mergedData, d)
	return mergedData


def readConfig(filePaths):
	yamlFiles = [projectRoot + '/data/defaultConfig.yml'] + filePaths
	config = {**getDefaultConfig(), **mergeFiles(yamlFiles)}

	config = _standardizeConfig(config)

	return {**config, 'scenarios': buildScenarios(config)}