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

from at.read_write.get_default_config import (
	get_default_config,
)

project_root = path.realpath(
	path.dirname(__file__) + '/../../..'
)

_dms_compact_re = re.compile(
	r'^(?P<deg>\d+)(?P<hemi>[NSEW])(?P<min>\d{2})(?P<sec>\d{2})?$'
)

default_scenarios = {'default': {}}


def _parse_date_string(date_str):
	parts = str(date_str).split('-')
	if len(parts) != 3:
		raise ValueError(f'Invalid date format: {date_str} (expected (YY)YY-MM-DD)')
	year_str, month_str, day_str = parts
	year = int(year_str)
	if len(year_str) == 2:
		year = 2000 + year
	elif len(year_str) != 4:
		raise ValueError(f'Invalid year width in date: {date_str}')
	return year, int(month_str), int(day_str)


def _parse_time_string(time_str):
	parts = str(time_str).split(':')
	if len(parts) != 3:
		raise ValueError(f'Invalid time format: {time_str} (expected hh:mm:ss)')
	hour, minute, second = map(int, parts)
	return hour, minute, second


def _parse_dms_value(value):
	if isinstance(value, (int, float)):
		return float(value)

	v = str(value).strip()
	if not v:
		raise ValueError('Empty coordinate string is invalid')

	m = _dms_compact_re.match(v)
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


def _utc_offset(config):
	return timezone(
		offset=timedelta(
			hours=config['utcHour'],
			minutes=config['utcMinute'],
		)
	)


def get_scenario_time(scenario, config):
	return datetime(
		scenario['year'], scenario['month'], scenario['day'],
		scenario['hour'], scenario['minute'], scenario['second'],
		tzinfo=_utc_offset(config),
	)


def _standardize_config(config):
	for key in ('latitude', 'longitude'):
		if key in config:
			config[key] = _parse_dms_value(config[key])

	if 'startDate' in config:
		config['year'], config['month'], config['day'] = _parse_date_string(config.pop('startDate'))
	if 'startTime' in config:
		config['hour'], config['minute'], config['second'] = _parse_time_string(config.pop('startTime'))

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

	start = get_scenario_time(config, config)
	config['date'] = start

	if 'endDate' in config and 'endTime' in config:
		year, month, day = _parse_date_string(config['endDate'])
		hour, minute, second = _parse_time_string(config['endTime'])
		end = datetime(year, month, day, hour, minute, second, tzinfo=_utc_offset(config))
		config['count'] = len(pd.date_range(
			start=start, end=end, freq=config['interval'], inclusive='both',
		))
	elif 'count' not in config:
		raise ValueError('count is required when endDate/endTime is not provided.')

	return config


def build_scenarios(config):
	scenarios = config.get('scenarios', default_scenarios)
	return {
		k: _standardize_config({**config, **scenario})
		for k, scenario in scenarios.items()
	}


merger = Merger(
	[(dict, ['merge'])],
	['override'],
	['override'],
)


def _normalize_imports(imports_value):
	if not imports_value:
		return []
	if isinstance(imports_value, str):
		return [imports_value]
	return list(imports_value)


def _format_import_cycle(import_stack, repeated_path):
	cycle_start = import_stack.index(repeated_path)
	cycle = import_stack[cycle_start:] + [repeated_path]
	return ' → '.join(cycle)


def _resolve_import_path(import_path, importing_file):
	return path.realpath(
		path.join(path.dirname(importing_file), import_path)
	)


def _load_file(file_path, import_stack):
	resolved_file_path = path.realpath(file_path)
	if resolved_file_path in import_stack:
		raise ValueError(
			'Config import cycle detected: '
			f'{_format_import_cycle(import_stack, resolved_file_path)}'
		)

	with open(resolved_file_path, 'r') as file:
		data = yaml.safe_load(file) or {}

	imports = _normalize_imports(data.pop('imports', []))
	if imports:
		data = merger.merge(
			_merge_files(
				[
					_resolve_import_path(import_path, resolved_file_path)
					for import_path in imports
				],
				import_stack + [resolved_file_path],
			),
			data,
		)

	return data


def _merge_files(file_paths, import_stack=None):
	import_stack = import_stack or []
	data = [
		_load_file(file, import_stack)
		for file in file_paths
	]
	if not data:
		return {}
	merged_data = data[0]
	for d in data[1:]:
		merged_data = merger.merge(merged_data, d)
	return merged_data


def merge_files(file_paths):
	return _merge_files(file_paths)


def read_config(file_paths):
	config = _merge_files([project_root + '/data/defaultConfig.yml'] + file_paths)
	config = {**get_default_config(), **config}

	if 'baseConfigurations' in config:
		base_config = config.pop('baseConfigurations') or {}
		config = {**base_config, **config}

	legacy_constants = config.pop('constants', {}) or {}
	computations = config.get('computations', {}) or {}
	if not isinstance(computations, dict):
		computations = {}
	if 'fields' in computations or 'constants' in computations:
		fields = computations.get('fields', {}) or {}
		constants = computations.get('constants', {}) or {}
	else:
		fields = {
			k: v
			for k, v in computations.items()
			if k not in ('constants', 'fields')
		}
		constants = {}
	config['computations'] = {
		'constants': {**legacy_constants, **constants},
		'fields': fields,
	}

	config.setdefault('report', {})
	config.setdefault('sources', [])

	config = _standardize_config(config)

	return {**config, 'scenarios': build_scenarios(config)}
