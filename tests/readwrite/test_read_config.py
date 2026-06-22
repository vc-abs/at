from pathlib import Path

from at.readWrite.readConfig import (
	buildEvents,
	getEventTime,
	mergeFiles,
	readConfig,
)


def test_get_event_time_applies_timezone_offset():
	config = {'utcHour': 5, 'utcMinute': 30}
	event = {
		'year': 2025,
		'month': 1,
		'day': 2,
		'hour': 3,
		'minute': 4,
		'second': 5,
	}
	dt = getEventTime(event, config)
	assert dt.utcoffset().total_seconds() == 19800
	assert (
		dt.year,
		dt.month,
		dt.day,
		dt.hour,
		dt.minute,
		dt.second,
	) == (2025, 1, 2, 3, 4, 5)


def test_build_events_merges_defaults_and_event_specific():
	config = {
		'latitude': 1.0,
		'longitude': 2.0,
		'year': 2025,
		'month': 1,
		'day': 2,
		'hour': 3,
		'minute': 4,
		'second': 5,
		'utcHour': 0,
		'utcMinute': 0,
		'events': {
			'default': {},
			'custom': {'hour': 8, 'name': 'c1'},
		},
	}
	events = buildEvents(config)

	assert events['default']['latitude'] == 1.0
	assert events['custom']['hour'] == 8
	assert events['custom']['name'] == 'c1'
	assert 'date' in events['custom']


def test_merge_files_merges_dicts(tmp_path: Path):
	f1 = tmp_path / 'a.yml'
	f2 = tmp_path / 'b.yml'
	f1.write_text('a: 1\nobj:\n  x: 1\n')
	f2.write_text('b: 2\nobj:\n  y: 2\n')

	merged = mergeFiles([str(f1), str(f2)])
	assert merged['a'] == 1
	assert merged['b'] == 2
	assert merged['obj'] == {'x': 1, 'y': 2}


def test_merge_files_merges_constants_nested_dicts(tmp_path: Path):
	f1 = tmp_path / 'a.yml'
	f2 = tmp_path / 'b.yml'
	f1.write_text(
		'constants:\n'
		'  marketing:\n'
		'    weekdays:\n'
		'      - wednesday\n'
		'    thresholds:\n'
		'      score: 250\n'
	)
	f2.write_text(
		'constants:\n'
		'  marketing:\n'
		'    thresholds:\n'
		'      score: 300\n'
		'      floor: 24\n'
	)

	merged = mergeFiles([str(f1), str(f2)])
	assert merged['constants'] == {
		'marketing': {
			'weekdays': ['wednesday'],
			'thresholds': {
				'score': 300,
				'floor': 24,
			},
		}
	}


def test_read_config_loads_default_and_user_files(tmp_path: Path):
	cfg = tmp_path / 'cfg.yml'
	cfg.write_text(
		'utcHour: 5\n'
		'utcMinute: 30\n'
		'events:\n'
		'  default:\n'
		'    hour: 9\n'
	)

	result = readConfig([str(cfg)])
	assert result['utcHour'] == 5
	assert result['constants'] == {}
	assert 'events' in result
	assert 'default' in result['events']
	assert 'date' in result['events']['default']
