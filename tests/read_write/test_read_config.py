from pathlib import Path

import pytest

from at.read_write.read_config import (
	build_scenarios,
	get_scenario_time,
	merge_files,
	read_config,
)


def test_get_scenario_time_applies_timezone_offset():
	config = {'utcHour': 5, 'utcMinute': 30}
	scenario = {
		'year': 2025,
		'month': 1,
		'day': 2,
		'hour': 3,
		'minute': 4,
		'second': 5,
	}
	dt = get_scenario_time(scenario, config)
	assert dt.utcoffset().total_seconds() == 19800
	assert (
		dt.year,
		dt.month,
		dt.day,
		dt.hour,
		dt.minute,
		dt.second,
	) == (2025, 1, 2, 3, 4, 5)


def test_build_scenarios_merges_defaults_and_scenario_specific():
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
		'interval': '1h',
		'count': 2,
		'scenarios': {
			'default': {},
			'custom': {'hour': 8, 'name': 'c1'},
		},
	}
	scenarios = build_scenarios(config)

	assert scenarios['default']['latitude'] == 1.0
	assert scenarios['custom']['hour'] == 8
	assert scenarios['custom']['name'] == 'c1'
	assert 'date' in scenarios['custom']
	assert scenarios['custom']['count'] == 2


def test_merge_files_merges_dicts(tmp_path: Path):
	f1 = tmp_path / 'a.yml'
	f2 = tmp_path / 'b.yml'
	f1.write_text('a: 1\nobj:\n  x: 1\n')
	f2.write_text('b: 2\nobj:\n  y: 2\n')

	merged = merge_files([str(f1), str(f2)])
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

	merged = merge_files([str(f1), str(f2)])
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
		'scenarios:\n'
		'  default:\n'
		'    hour: 9\n'
	)

	result = read_config([str(cfg)])
	assert result['utcHour'] == 5
	assert result['computations'] == {'constants': {}, 'fields': {}}
	assert 'scenarios' in result
	assert 'default' in result['scenarios']
	assert 'date' in result['scenarios']['default']



def test_read_config_supports_single_import(tmp_path: Path):
	base = tmp_path / 'base.yml'
	child = tmp_path / 'child.yml'
	base.write_text(
		'interval: 1h\n'
		'count: 1\n'
		'report:\n'
		'  order:\n'
		'    score: ascending\n'
	)
	child.write_text(
		'imports:\n'
		'  - base.yml\n'
		'report:\n'
		'  order:\n'
		'    score: descending\n'
		'computations:\n'
		'  score: h1 + h2\n'
	)

	assert merge_files([str(child)]) == merge_files([str(base), str(child)])



def test_read_config_supports_chained_imports(tmp_path: Path):
	a = tmp_path / 'a.yml'
	b = tmp_path / 'b.yml'
	c = tmp_path / 'c.yml'
	a.write_text(
		'interval: 1h\n'
		'count: 1\n'
		'nested:\n'
		'  left: a\n'
		'  shared: a\n'
	)
	b.write_text(
		'imports:\n'
		'  - a.yml\n'
		'nested:\n'
		'  shared: b\n'
	)
	c.write_text(
		'imports:\n'
		'  - b.yml\n'
		'nested:\n'
		'  right: c\n'
	)

	result = read_config([str(c)])
	assert result['nested'] == {'left': 'a', 'shared': 'b', 'right': 'c'}



def test_read_config_supports_multi_import_merge_order(tmp_path: Path):
	a = tmp_path / 'a.yml'
	b = tmp_path / 'b.yml'
	c = tmp_path / 'c.yml'
	a.write_text(
		'interval: 1h\n'
		'count: 1\n'
		'flag: a\n'
	)
	b.write_text(
		'flag: b\n'
		'obj:\n'
		'  left: 1\n'
	)
	c.write_text(
		'imports:\n'
		'  - a.yml\n'
		'  - b.yml\n'
		'flag: c\n'
		'obj:\n'
		'  right: 2\n'
	)

	result = read_config([str(c)])
	assert result['flag'] == 'c'
	assert result['obj'] == {'left': 1, 'right': 2}



def test_read_config_resolves_imports_relative_to_file(tmp_path: Path):
	nested = tmp_path / 'nested'
	sibling = tmp_path / 'sibling.yml'
	child = nested / 'child.yml'
	nested.mkdir()
	sibling.write_text(
		'interval: 1h\n'
		'count: 1\n'
		'flag: sibling\n'
	)
	child.write_text(
		'imports:\n'
		'  - ../sibling.yml\n'
		'flag: child\n'
	)

	result = read_config([str(child)])
	assert result['flag'] == 'child'



def test_read_config_rejects_import_cycles(tmp_path: Path):
	a = tmp_path / 'a.yml'
	b = tmp_path / 'b.yml'
	a.write_text(
		'interval: 1h\n'
		'count: 1\n'
		'imports:\n'
		'  - b.yml\n'
	)
	b.write_text(
		'imports:\n'
		'  - a.yml\n'
	)

	with pytest.raises(ValueError, match='Config import cycle detected: .*a.yml.*b.yml.*a.yml'):
		read_config([str(a)])



def test_read_config_strips_imports_key(tmp_path: Path):
	base = tmp_path / 'base.yml'
	child = tmp_path / 'child.yml'
	base.write_text(
		'interval: 1h\n'
		'count: 1\n'
		'imports:\n'
		'  - child.yml\n'
	)
	child.write_text(
		'flag: child\n'
	)

	result = read_config([str(child)])
	assert 'imports' not in result



def test_read_config_loads_default_and_user_files_against_imports_once(tmp_path: Path):
	base = tmp_path / 'base.yml'
	child = tmp_path / 'child.yml'
	base.write_text(
		'interval: 1h\n'
		'count: 1\n'
	)
	child.write_text(
		'imports:\n'
		'  - base.yml\n'
	)

	result = read_config([str(child)])
	assert result['utcHour'] == 5
	assert result['utcMinute'] == 30
	assert result['sources'] == [
		'muhurtaYogaEffects',
		'objectHouses',
		'planetaryDegrees',
		'ashtakavarga',
		'mahaDasha',
		'antarDashas',
		'planetFlags',
		'planetQualities',
		'timeFlags',
		'gowriFlags',
		'shadBalaStrength',
		'karakas',
		'scenario',
		'panchang',
	]


def test_dms_compact_parses_to_decimal(repo_root):
	cfg = read_config([str(repo_root / 'tests/fixtures/coord_sampling_base.yml')])
	assert cfg['latitude'] == pytest.approx(70 + 15 / 60)
	assert cfg['longitude'] == pytest.approx(15 + 59 / 60 + 30 / 3600)


def test_decimal_degrees_pass_through(repo_root):
	cfg = read_config([str(repo_root / 'tests/fixtures/coord_sampling_enddate.yml')])
	assert cfg['latitude'] == pytest.approx(23.101)
	assert cfg['longitude'] == pytest.approx(77.461)


def test_legacy_frequency_periods_normalized_to_count_interval(repo_root):
	cfg = read_config([str(repo_root / 'tests/fixtures/coord_sampling_legacy.yml')])
	assert cfg['interval'] == '1h'
	assert cfg['count'] == 2
	assert 'frequency' not in cfg
	assert 'periods' not in cfg


def test_start_date_time_aliases_base_inputs(repo_root):
	cfg = read_config([str(repo_root / 'tests/fixtures/coord_sampling_enddate.yml')])
	assert (cfg['year'], cfg['month'], cfg['day']) == (2024, 4, 1)
	assert (cfg['hour'], cfg['minute'], cfg['second']) == (0, 0, 0)


def test_end_datetime_derives_count_both_inclusive(repo_root):
	cfg = read_config([str(repo_root / 'tests/fixtures/coord_sampling_enddate.yml')])
	scenario = cfg['scenarios']['default']
	assert scenario['count'] == 3


def test_explicit_count_matching_derived_length_is_accepted(tmp_path):
	f = tmp_path / 'match.yml'
	f.write_text(
		'latitude: 23.101\n'
		'longitude: 77.461\n'
		'startDate: 2024-04-01\n'
		'startTime: 00:00:00\n'
		'endDate: 2024-04-01\n'
		'endTime: 02:00:00\n'
		'interval: 1h\n'
		'count: 3\n'
	)
	cfg = read_config([str(f)])
	assert cfg['scenarios']['default']['count'] == 3


def test_end_window_overrides_conflicting_count(tmp_path):
	f = tmp_path / 'mismatch.yml'
	f.write_text(
		'latitude: 23.101\n'
		'longitude: 77.461\n'
		'startDate: 2024-04-01\n'
		'startTime: 00:00:00\n'
		'endDate: 2024-04-01\n'
		'endTime: 02:00:00\n'
		'interval: 1h\n'
		'count: 5\n'
	)
	cfg = read_config([str(f)])
	assert cfg['scenarios']['default']['count'] == 3
	assert cfg['count'] == 3


def test_invalid_dms_string_raises(repo_root):
	with pytest.raises(ValueError):
		read_config([str(repo_root / 'tests/fixtures/coord_sampling_invalid_dms.yml')])


def test_variable_calendar_interval_rejected(repo_root):
	with pytest.raises(ValueError):
		read_config([str(repo_root / 'tests/fixtures/coord_sampling_variable_interval.yml')])


def test_partial_end_date_time_raises(tmp_path):
	f = tmp_path / 'partial.yml'
	f.write_text(
		'latitude: 23.101\n'
		'longitude: 77.461\n'
		'interval: 1h\n'
		'count: 1\n'
		'endDate: 2024-04-01\n'
	)
	with pytest.raises(ValueError):
		read_config([str(f)])


