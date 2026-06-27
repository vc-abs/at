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


# --- imports: directive resolution ---


def test_single_import_overlays_own_body(tmp_path):
	base = tmp_path / 'base.yml'
	this = tmp_path / 'this.yml'
	base.write_text('a: 1\nshared: base\n')
	this.write_text('imports: [base.yml]\nb: 2\nshared: this\n')

	resolved = _load_with_imports(str(this))
	expected = merge_files([str(base), str(this)])
	expected.pop('imports', None)
	assert resolved == expected
	assert resolved == {'a': 1, 'b': 2, 'shared': 'this'}


def test_chained_imports_resolve_depth_first(tmp_path):
	a = tmp_path / 'a.yml'
	b = tmp_path / 'b.yml'
	c = tmp_path / 'c.yml'
	a.write_text('val: a\nonlyA: 1\n')
	b.write_text('imports: [a.yml]\nval: b\nonlyB: 2\n')
	c.write_text('imports: [b.yml]\nval: c\nonlyC: 3\n')

	resolved = _load_with_imports(str(c))
	assert resolved['val'] == 'c'
	assert resolved['onlyA'] == 1
	assert resolved['onlyB'] == 2
	assert resolved['onlyC'] == 3


def test_multi_import_merge_order_rightmost_wins(tmp_path):
	a = tmp_path / 'a.yml'
	b = tmp_path / 'b.yml'
	this = tmp_path / 'this.yml'
	a.write_text('val: a\nkeepA: 1\n')
	b.write_text('val: b\nkeepB: 2\n')
	this.write_text('imports: [a.yml, b.yml]\nval: this\n')

	resolved = _load_with_imports(str(this))
	expected = merge_files([str(a), str(b), str(this)])
	expected.pop('imports', None)
	assert resolved == expected
	assert resolved['val'] == 'this'
	assert resolved['keepA'] == 1
	assert resolved['keepB'] == 2


def test_imports_resolve_relative_to_importing_file_dir(tmp_path):
	sub = tmp_path / 'sub'
	sub.mkdir()
	sibling = tmp_path / 'sibling.yml'
	this = sub / 'this.yml'
	sibling.write_text('fromSibling: "yes"\n')
	this.write_text('imports: [../sibling.yml]\nlocal: 1\n')

	resolved = _load_with_imports(str(this))
	assert resolved['fromSibling'] == 'yes'
	assert resolved['local'] == 1


def test_import_cycle_raises_naming_cycle(tmp_path):
	a = tmp_path / 'a.yml'
	b = tmp_path / 'b.yml'
	a.write_text('imports: [b.yml]\n')
	b.write_text('imports: [a.yml]\n')

	with pytest.raises(ValueError) as exc:
		_load_with_imports(str(a))
	msg = str(exc.value)
	assert 'cycle' in msg
	assert 'a.yml' in msg
	assert 'b.yml' in msg


def test_imports_key_stripped_from_result(tmp_path):
	base = tmp_path / 'base.yml'
	this = tmp_path / 'this.yml'
	base.write_text('x: 1\n')
	this.write_text('imports: [base.yml]\ny: 2\n')

	resolved = _load_with_imports(str(this))
	assert 'imports' not in resolved


def test_read_config_default_precedence_unchanged_with_imports(tmp_path):
	base = tmp_path / 'base.yml'
	this = tmp_path / 'this.yml'
	base.write_text('interval: 2h\n')
	this.write_text('imports: [base.yml]\nlatitude: 23.101\nlongitude: 77.461\ninterval: 1h\ncount: 2\n')

	cfg = read_config([str(this)])
	# defaultConfig provides interval: 1h; the import does not bypass it,
	# and the importing file's own interval wins over both.
	assert cfg['interval'] == '1h'
	# defaults (ayanamsa, utcHour) are still present from defaultConfig.
	assert cfg['utcHour'] == 5
	assert cfg['utcMinute'] == 30
	assert 'imports' not in cfg


def test_read_config_imports_compose_with_scenarios(tmp_path):
	base = tmp_path / 'base.yml'
	this = tmp_path / 'this.yml'
	base.write_text(
		'latitude: 23.101\n'
		'longitude: 77.461\n'
		'interval: 1h\n'
		'count: 2\n'
		'scenarios:\n'
		'  default: {}\n'
		'  shared:\n'
		'    hour: 6\n'
		'    name: shared\n'
	)
	this.write_text(
		'imports: [base.yml]\n'
		'scenarios:\n'
		'  shared:\n'
		'    name: overridden\n'
	)

	cfg = read_config([str(this)])
	assert 'shared' in cfg['scenarios']
	assert cfg['scenarios']['shared']['hour'] == 6
	assert cfg['scenarios']['shared']['name'] == 'overridden'


