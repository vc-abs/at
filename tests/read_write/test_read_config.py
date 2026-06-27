from pathlib import Path

import pytest

from at.read_write.read_config import (
	_load_with_imports,
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


def _write(path, text):
	path.write_text(text)
	return path


def test_imports_single_import_overlays_own_body(tmp_path):
	base = _write(tmp_path / 'base.yml', 'computations:\n  constants:\n    a: 1\n    b: 2\n')
	_write(
		tmp_path / 'child.yml',
		'imports: [base.yml]\ncomputations:\n  constants:\n    b: 20\n    c: 3\n',
	)
	# Reference: the child's own body (imports stripped) stacked over the base.
	child_body = _write(
		tmp_path / 'child_body.yml',
		'computations:\n  constants:\n    b: 20\n    c: 3\n',
	)
	resolved = _load_with_imports(str(tmp_path / 'child.yml'))
	assert resolved == {'computations': {'constants': {'a': 1, 'b': 20, 'c': 3}}}
	assert resolved == merge_files([str(base), str(child_body)])


def test_imports_chained_depth_first_child_wins(tmp_path):
	_write(tmp_path / 'a.yml', 'computations:\n  constants:\n    x: 1\n    y: 1\n')
	_write(tmp_path / 'b.yml', 'imports: [a.yml]\ncomputations:\n  constants:\n    y: 2\n    z: 2\n')
	c = _write(
		tmp_path / 'c.yml',
		'imports: [b.yml]\ncomputations:\n  constants:\n    z: 3\n',
	)
	resolved = _load_with_imports(str(c))
	assert resolved['computations']['constants'] == {'x': 1, 'y': 2, 'z': 3}


def test_imports_multi_merge_order_rightmost_wins(tmp_path):
	_write(tmp_path / 'a.yml', 'computations:\n  constants:\n    k: 1\n')
	_write(tmp_path / 'b.yml', 'computations:\n  constants:\n    k: 2\n')
	_write(
		tmp_path / 'this.yml',
		'imports: [a.yml, b.yml]\ncomputations:\n  constants:\n    k: 3\n',
	)
	# Reference: a, b, then this's own body (imports stripped) stacked on top.
	this_body = _write(
		tmp_path / 'this_body.yml',
		'computations:\n  constants:\n    k: 3\n',
	)
	resolved = _load_with_imports(str(tmp_path / 'this.yml'))
	assert resolved['computations']['constants']['k'] == 3
	assert resolved == merge_files(
		[str(tmp_path / 'a.yml'), str(tmp_path / 'b.yml'), str(this_body)]
	)


def test_imports_resolve_relative_to_importing_file_dir(tmp_path):
	sub = tmp_path / 'sub'
	sub.mkdir()
	_write(tmp_path / 'sibling.yml', 'computations:\n  constants:\n    s: 9\n')
	inner = _write(
		sub / 'inner.yml',
		'imports: [../sibling.yml]\ncomputations:\n  constants:\n    s: 90\n',
	)
	# CWD is tmp_path, not sub; relative-to-file resolution still finds sibling.
	resolved = _load_with_imports(str(inner))
	assert resolved['computations']['constants']['s'] == 90


def test_imports_cycle_rejected_with_named_chain(tmp_path):
	_write(tmp_path / 'a.yml', 'imports: [b.yml]\n')
	_write(tmp_path / 'b.yml', 'imports: [a.yml]\n')
	with pytest.raises(ValueError, match='Import cycle detected'):
		_load_with_imports(str(tmp_path / 'a.yml'))


def test_imports_key_stripped_from_merged_result(tmp_path):
	_write(tmp_path / 'base.yml', 'computations:\n  constants:\n    a: 1\n')
	child = _write(tmp_path / 'child.yml', 'imports: [base.yml]\ncomputations:\n  constants:\n    b: 2\n')
	resolved = _load_with_imports(str(child))
	assert 'imports' not in resolved


def test_imports_default_config_precedence_unchanged(tmp_path):
	# defaultConfig.yml supplies interval/count; an import must not bypass it.
	_write(
		tmp_path / 'base.yml',
		'computations:\n  constants:\n    shared: 1\n',
	)
	child = _write(
		tmp_path / 'child.yml',
		'imports: [base.yml]\ninterval: 1h\ncount: 1\nlatitude: 13.0827\nlongitude: 80.2707\n',
	)
	cfg = read_config([str(child)])
	assert cfg['interval'] == '1h'
	assert cfg['count'] == 1
	# The imported constant survives into the merged computations.
	assert cfg['computations']['constants']['shared'] == 1


def test_imports_compose_with_scenarios_deep_merge(tmp_path):
	_write(
		tmp_path / 'base.yml',
		'scenarios:\n  default:\n    interval: 1h\n  fast:\n    interval: 30min\n'
	)
	child = _write(
		tmp_path / 'child.yml',
		'imports: [base.yml]\nscenarios:\n  fast:\n    count: 2\nlatitude: 13.0827\nlongitude: 80.2707\ninterval: 1h\ncount: 1\n',
	)
	cfg = read_config([str(child)])
	assert cfg['scenarios']['fast']['interval'] == '30min'
	assert cfg['scenarios']['fast']['count'] == 2


