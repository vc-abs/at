from datetime import datetime, timezone

import pandas as pd

from at.read_write.read_config import read_config
from at.tools.generate_combos import (
	add_columns,
	add_custom_columns,
	format_dasha_data,
	generate_combos,
	generate_scenario_combos,
	get_column,
	get_computation_constants,
	get_computation_fields,
	get_expression_locals,
	get_gowri_flags,
	get_panchang,
	get_fields,
	get_planetary_degrees,
	get_planet_flags_by_planet,
	get_planet_qualities,
	get_time_flags,
	process_summary_column,
	resolve_constant_reference,
	rewrite_constants_expression,
	sort_data,
	split_timestamp,
)


class _dummy_panchang:
	def __init__(self):
		self.tithi = 1
		self.vaara = 'wednesday'
		self.rise_and_set = {
			'sunrise': datetime(
				2025,
				1,
				1,
				6,
				0,
				0,
				tzinfo=timezone.utc,
			),
			'sunset': datetime(
				2025,
				1,
				1,
				18,
				0,
				0,
				tzinfo=timezone.utc,
			),
		}
		self.gowri = {
			'gowri': 'laabam',
			'gowriScore': 1,
			'gowriM': 'gain',
			'gowriS': 1,
			'gowriT': 'day',
			'gowriStart': datetime(
				2025,
				1,
				1,
				6,
				0,
				0,
				tzinfo=timezone.utc,
			),
			'gowriEnd': datetime(
				2025,
				1,
				1,
				7,
				30,
				0,
				tzinfo=timezone.utc,
			),
			'gowriF': 'day|laabam',
		}


class _dummy_chart:
	def __init__(self, objects, event_time=None):
		self.objects = objects
		self.panchang = _dummy_panchang()
		self.config = {
			'datetime': event_time
			or datetime(
				2025,
				1,
				1,
				12,
				30,
				0,
				tzinfo=timezone.utc,
			),
		}


class _panchang_obj:
	def __init__(self):
		self.rise_and_set = {
			'sunrise': datetime(
				2025,
				1,
				1,
				6,
				0,
				0,
				tzinfo=timezone.utc,
			),
			'sunset': datetime(
				2025,
				1,
				1,
				18,
				0,
				0,
				tzinfo=timezone.utc,
			),
		}
		self.tithi = 1
		self.nakshatra = 'asvini'
		self.vaara = 'sunday'
		self.gowri = {
			'gowri': 'laabam',
			'gowriScore': 1,
			'gowriM': 'gain',
			'gowriS': 1,
			'gowriT': 'day',
			'gowriStart': datetime(
				2025,
				1,
				1,
				6,
				0,
				0,
				tzinfo=timezone.utc,
			),
			'gowriEnd': datetime(
				2025,
				1,
				1,
				7,
				30,
				0,
				tzinfo=timezone.utc,
			),
			'gowriF': 'day|laabam',
		}


class _panchang_chart:
	def __init__(self):
		self.panchang = _panchang_obj()



def _chart_objects_for_flags():
	return {
		'asc': {'longitude': 100.0, 'sign': 4, 'house': 1, 'type': 'angle', 'name': 'asc'},
		'sun': {'longitude': 100.0, 'retrograde': False, 'type': 'planet', 'name': 'sun', 'house': 5},
		'moon': {'longitude': 111.0, 'retrograde': False, 'type': 'planet', 'name': 'moon', 'house': 5},
		'mars': {'longitude': 120.0, 'retrograde': False, 'type': 'planet', 'name': 'mars', 'house': 5},
		'mercury': {'longitude': 102.0, 'retrograde': True, 'type': 'planet', 'name': 'mercury', 'house': 5},
		'jupiter': {'longitude': 180.0, 'retrograde': True, 'type': 'planet', 'name': 'jupiter', 'house': 6},
		'venus': {'longitude': 109.0, 'retrograde': False, 'type': 'planet', 'name': 'venus', 'house': 5},
		'saturn': {'longitude': 250.0, 'retrograde': True, 'type': 'planet', 'name': 'saturn', 'house': 8},
		'rahu': {'longitude': 220.0, 'retrograde': True, 'type': 'planet', 'name': 'rahu', 'house': 9},
		'ketu': {'longitude': 40.0, 'retrograde': True, 'type': 'planet', 'name': 'ketu', 'house': 3},
	}



def test_planet_flags_are_pipe_sorted_and_compact():
	chart = _dummy_chart(_chart_objects_for_flags())

	# mercury: retrograde + within 14 degrees of sun -> C|R
	assert get_planet_flags_by_planet(chart, 'mercury') == 'C|R'
	# moon: combust only
	assert get_planet_flags_by_planet(chart, 'moon') == 'C'
	# jupiter: retro only (too far from sun)
	assert get_planet_flags_by_planet(chart, 'jupiter') == 'R'



def test_planetary_degrees_include_asc_and_nodes_in_order():
	chart = _dummy_chart(_chart_objects_for_flags())
	degrees = get_planetary_degrees(chart)

	keys = list(degrees.keys())
	assert keys[0] == 'asD'
	assert keys[-2:] == ['raD', 'keD']
	assert degrees['asD'] == 100.0
	assert degrees['raD'] == 220.0
	assert degrees['keD'] == 40.0



def test_planet_qualities_include_all_planets_with_expected_values():
	chart = _dummy_chart(_chart_objects_for_flags())
	qualities = get_planet_qualities(chart)

	assert qualities['suQ'] == 'malefic'
	assert qualities['moQ'] == 'malefic'
	assert qualities['maQ'] == 'malefic'
	assert qualities['meQ'] == 'malefic'
	assert qualities['juQ'] == 'benefic'
	assert qualities['veQ'] == 'benefic'
	assert qualities['saQ'] == 'malefic'



def test_time_flags_encode_active_day_segment_markers():
	chart = _dummy_chart(
		_chart_objects_for_flags(),
		event_time=datetime(
			2025,
			1,
			1,
			12,
			30,
			0,
			tzinfo=timezone.utc,
		),
	)
	flags = get_time_flags(chart)

	assert flags['timeF'] == 'RK'



def test_time_flags_are_empty_outside_marked_segments():
	chart = _dummy_chart(
		_chart_objects_for_flags(),
		event_time=datetime(
			2025,
			1,
			1,
			6,
			30,
			0,
			tzinfo=timezone.utc,
		),
	)
	flags = get_time_flags(chart)

	assert flags['timeF'] == ''



def test_format_dasha_data_uses_placeholder_when_bala_missing():
	dasha = {
		'lord': 'rahu',
		'startsAt': datetime(2025, 1, 1, tzinfo=timezone.utc),
		'endsAt': datetime(2026, 1, 1, tzinfo=timezone.utc),
		'remainder': 0.5,
	}
	balas = {}
	out = format_dasha_data(dasha, balas, 'md')

	assert out['mdLord'] == 'rahu'
	assert out['mdlStrength'] == 0
	assert out['mdlIshtaPhala'] == 0



def test_get_column_supports_str_expression_and_dict_summary():
	df = pd.DataFrame([{'a': 1, 'b': 2}])
	config = {'constants': {}}
	assert get_column(df, 'a + b', config).iloc[0] == 3
	assert get_column(df, {'sum': ['a', 'b']}, config).iloc[0] == 3



def test_get_column_returns_unsupported_values_unchanged():
	df = pd.DataFrame([{'a': 1}])
	value = ['a']
	assert get_column(df, value, {'constants': {}}) is value



def test_process_summary_column_directly():
	df = pd.DataFrame(
		[
			{'x': 2, 'y': 3},
			{'x': 4, 'y': 5},
		]
	)
	res = process_summary_column(
		df,
		{'sum': ['x', 'y']},
		{'constants': {}},
	)
	assert list(res) == [5, 9]



def test_add_custom_columns_adds_each_declared_column():
	df = pd.DataFrame([{'a': 1, 'b': 2}])
	add_custom_columns(
		df,
		{
			'c': 'a + b',
			'd': {'sum': ['a', 'b']},
		},
		{'constants': {}},
	)
	assert list(df.columns) == ['a', 'b', 'c', 'd']
	assert df['c'].iloc[0] == 3
	assert df['d'].iloc[0] == 3



def test_rewrite_constants_expression_marks_namespace_for_pandas():
	assert rewrite_constants_expression(
		'vaara.isin(constants.marketingWeekdays)'
	) == 'vaara.isin(@constants.marketingWeekdays)'
	assert rewrite_constants_expression(
		'constants.thresholds.score >= 300'
	) == '@constants.thresholds.score >= 300'
	assert rewrite_constants_expression(
		'vaara.isin(@constants.marketingWeekdays)'
	) == 'vaara.isin(@constants.marketingWeekdays)'



def test_get_expression_locals_exposes_constants_namespace():
	locals_ = get_expression_locals(
		{
			'constants': {
				'marketingWeekdays': ['wednesday', 'friday'],
				'thresholds': {'score': 300},
			},
		}
	)
	constants = locals_['constants']
	assert constants.marketingWeekdays == ['wednesday', 'friday']
	assert constants.thresholds.score == 300



def test_get_expression_locals_exposes_mapping_constants_for_map_usage():
	locals_ = get_expression_locals(
		{
			'constants': {
				'marketingWeekdayWeights': {
					'wednesday': 30,
					'friday': 24,
				},
			},
		}
	)
	constants = locals_['constants']
	assert constants.marketingWeekdayWeights['wednesday'] == 30
	assert constants.marketingWeekdayWeights.friday == 24



def test_get_column_supports_constants_namespace_expression():
	df = pd.DataFrame([{'a': 1, 'b': 2}])
	config = {'constants': {'weights': {'a': 10, 'b': 100}}}
	result = get_column(
		df,
		'a * constants.weights.a + b * constants.weights.b',
		config,
	)
	assert result.iloc[0] == 210



def test_process_summary_column_resolves_constant_reference_list():
	df = pd.DataFrame(
		[
			{'h3': 22, 'h5': 25, 'h7': 24},
			{'h3': 29, 'h5': 27, 'h7': 26},
		]
	)
	config = {
		'constants': {
			'marketingMinHouses': ['h3', 'h5', 'h7'],
		}
	}
	res = process_summary_column(
		df,
		{'min': 'constants.marketingMinHouses'},
		config,
	)
	assert list(res) == [22, 26]



def test_resolve_constant_reference_returns_non_constant_strings_unchanged():
	config = {'constants': {'x': ['a']}}
	assert resolve_constant_reference(['h1'], config) == ['h1']
	assert resolve_constant_reference('h1', config) == 'h1'



def test_add_custom_columns_supports_constants_and_does_not_export_them():
	df = pd.DataFrame(
		[
			{'vaara': 'wednesday', 'h3': 22, 'h5': 25, 'h7': 24},
		]
	)
	config = {
		'constants': {
			'marketingWeekdays': ['wednesday', 'friday'],
			'marketingMinHouses': ['h3', 'h5', 'h7'],
		}
	}
	add_custom_columns(
		df,
		{
			'isMarketingWeekday': 'vaara.isin(constants.marketingWeekdays)',
			'marketingMin': {
				'min': 'constants.marketingMinHouses',
			},
		},
		config,
	)
	assert list(df.columns) == [
		'vaara',
		'h3',
		'h5',
		'h7',
		'isMarketingWeekday',
		'marketingMin',
	]
	assert bool(df['isMarketingWeekday'].iloc[0]) is True
	assert df['marketingMin'].iloc[0] == 22
	assert 'constants' not in df.columns



def test_add_custom_columns_supports_mapping_constants_with_series_map():
	df = pd.DataFrame(
		[
			{'vaara': 'wednesday'},
			{'vaara': 'friday'},
			{'vaara': 'monday'},
		]
	)
	config = {
		'constants': {
			'marketingWeekdayWeights': {
				'wednesday': 30,
				'friday': 24,
				'thursday': 22,
				'sunday': 18,
			},
		}
	}
	add_custom_columns(
		df,
		{
			'weekdayScore': (
				'vaara.map(constants.marketingWeekdayWeights).fillna(0)'
			),
		},
		config,
	)
	assert list(df['weekdayScore']) == [30.0, 24.0, 0.0]



def test_muhurta_base_defines_shared_constants_pattern(repo_root):
	import yaml
	with open(repo_root / 'presets/muhurta-base.yml', 'r') as f:
		text = f.read()
		parsed = yaml.safe_load(text)

	assert 'imports' not in parsed  # the base is imported, never imports
	assert 'vaara.map(constants.eventWeekdayWeights).fillna(0)' in text
	assert 'mdLord.isin(constants.eventCorePlanets)' in text
	assert 'min: constants.eventMinHouses' in text
	assert 'mean: constants.eventStrengthCols' in text
	# the shared report keys on the canonical eventScore column.
	assert 'eventScore: descending' in text
	assert 'baseEventScore: descending' in text
	assert 'eventMin >= constants.eventMinThreshold' in text
	assert 'eventScore >= constants.eventScoreThreshold' in text


def test_launch_preset_imports_base_and_supplies_constants(repo_root):
	with open(repo_root / 'presets/events/launch.yml', 'r') as f:
		text = f.read()

	assert 'imports: [../muhurta-base.yml]' in text
	assert 'eventWeekdayWeights:' in text
	assert 'eventCorePlanets:' in text
	assert 'eventMinHouses:' in text
	assert 'eventHouseScore:' in text
	assert 'baseEventScore:' in text
	assert 'eventScore:' in text
	# the shared formula text lives in the base, not the event file.
	assert 'vaara.map(constants.eventWeekdayWeights)' not in text



def test_staff_onboarding_preset_imports_base_and_supplies_constants(repo_root):
	with open(repo_root / 'presets/events/staffOnboarding.yml', 'r') as f:
		text = f.read()

	assert 'imports: [../muhurta-base.yml]' in text
	assert 'eventWeekdayWeights:' in text
	assert 'eventCorePlanets:' in text
	assert 'eventMinHouses:' in text
	assert 'eventHouseScore:' in text
	assert 'baseEventScore:' in text
	assert 'eventScore:' in text
	# staff's strength average uses Venus (meS/veS/moS/juS/suS), like
	# marketing/launch; Saturn appears in the dasha core-planet list, not here.
	assert 'veS' in text
	assert 'saS' not in text



def test_student_onboarding_preset_imports_base_and_supplies_constants(repo_root):
	with open(repo_root / 'presets/events/studentOnboarding.yml', 'r') as f:
		text = f.read()

	assert 'imports: [../muhurta-base.yml]' in text
	assert 'eventWeekdayWeights:' in text
	assert 'eventCorePlanets:' in text
	assert 'eventMinHouses:' in text
	assert 'eventHouseScore:' in text
	assert 'baseEventScore:' in text
	assert 'eventScore:' in text
	# student nulls out the full-moon tithi bonus via a constant.
	assert 'eventFullMoonBonus: 0' in text



def test_sort_data_and_split_timestamp_mutate_dataframe():
	df = pd.DataFrame(
		[
			{
				'scenario': 'e',
				'timestamp': datetime(
					2025,
					1,
					2,
					1,
					tzinfo=timezone.utc,
				),
				'score': 1,
			},
			{
				'scenario': 'e',
				'timestamp': datetime(
					2025,
					1,
					1,
					1,
					tzinfo=timezone.utc,
				),
				'score': 2,
			},
		]
	)

	sort_data(df, {'score': 'descending'})
	assert list(df['score']) == [2, 1]

	split_timestamp(df)
	assert 'timestamp' not in df.columns
	assert list(df.columns[:2]) == ['date', 'time']



def test_sort_data_is_stable_for_tied_scores():
	# A stable sort keeps tied rows in their original relative order.
	# Use enough rows that quicksort would otherwise reshuffle the tie block.
	labels = [chr(65 + i) for i in range(17)]
	df = pd.DataFrame(
		{
			'label': labels,
			'score': [2] * 8 + [1] * 9,
		}
	)

	sort_data(df, {'score': 'descending'})

	# High-score tie block (8 rows) must retain input order A..H.
	assert list(df['label'])[:8] == labels[:8]
	# Low-score tie block (9 rows) must retain input order I..Q.
	assert list(df['label'])[8:] == labels[8:]



def test_get_panchang_formats_time_strings():
	result = get_panchang(_panchang_chart())
	assert result['sunrise'] == '06:00:00'
	assert result['sunset'] == '18:00:00'
	assert result['tithi'] == 1
	assert result['nakshatra'] == 'asvini'
	assert result['vaara'] == 'sunday'



def test_get_fields_honors_sources_filter():
	chart = _panchang_chart()
	fields = get_fields(chart, ['panchang'])

	assert 'tithi' in fields
	assert 'suF' not in fields
	assert 'asD' not in fields



def test_get_gowri_flags_formats_compact_fields():
	result = get_gowri_flags(_panchang_chart())
	assert result['gowri'] == 'laabam'
	assert result['gowriScore'] == 1
	assert result['gowriStart'] == '06:00:00'
	assert result['gowriEnd'] == '07:30:00'
	assert result['gowriF'] == 'day|laabam'



def test_add_columns_supports_all_none_and_some_selectors():
	df = pd.DataFrame(
		[
			{
				'scenario': 'default',
				'date': '2025-01-01',
				'time': '00:00:00',
				'suD': 10.0,
				'moD': 20.0,
				'asD': 5.0,
				'suF': 'R',
				'suQ': 'malefic',
				'timeF': 'RK',
				'gowri': 'laabam',
				'gowriScore': 1,
				'gowriF': 'day|laabam',
				'avgIP': 30.0,
			}
		]
	)

	selected = add_columns(
		df,
		{
			'scenario': 'all',
			'planetaryDegrees': ['asD', 'suD'],
			'planetFlags': 'none',
			'planetQualities': ['suQ'],
			'timeFlags': ['timeF'],
			'gowriFlags': ['gowri', 'gowriScore', 'gowriF'],
			'shadBalaStrength': ['avgIP'],
		},
	)

	assert list(selected.columns) == [
		'scenario',
		'date',
		'time',
		'asD',
		'suD',
		'suQ',
		'timeF',
		'gowri',
		'gowriScore',
		'gowriF',
		'avgIP',
	]



def test_add_columns_keeps_fieldset_order():
	df = pd.DataFrame(
		[
			{
				'scenario': 'e',
				'date': '2025-01-01',
				'time': '00:00:00',
				'suF': 'C',
				'moF': '',
				'asD': 1.0,
				'suD': 2.0,
			}
		]
	)

	selected = add_columns(
		df,
		{
			'planetFlags': ['suF', 'moF'],
			'planetaryDegrees': ['asD', 'suD'],
		},
	)

	assert list(selected.columns) == ['suF', 'moF', 'asD', 'suD']



def test_add_columns_can_select_computations_explicitly():
	df = pd.DataFrame(
		[
			{
				'scenario': 'e',
				'date': '2025-01-01',
				'time': '00:00:00',
				'weekdayScore': 30.0,
				'eventScore': 317.0,
				'eventHouseScore': 91.0,
			}
		]
	)

	selected = add_columns(
		df,
		{
			'computations': ['eventScore', 'weekdayScore'],
			'scenario': 'all',
		},
	)

	assert list(selected.columns) == ['eventScore', 'weekdayScore', 'scenario', 'date', 'time']


# --- per-scenario constants & computations ---


def test_groupby_transform_string_produces_per_group_zscore():
	df = pd.DataFrame([
		{'scenario': 'a', 'eventScore': 1},
		{'scenario': 'a', 'eventScore': 2},
		{'scenario': 'a', 'eventScore': 3},
		{'scenario': 'b', 'eventScore': 10},
		{'scenario': 'b', 'eventScore': 20},
		{'scenario': 'b', 'eventScore': 30},
	])
	add_custom_columns(df, {
		'eventScoreDev': "(eventScore - eventScore.groupby(scenario).transform('mean'))"
		                 " / eventScore.groupby(scenario).transform('std')",
	}, {'computations': {'constants': {}, 'fields': {}}})
	# per-group z-score, ddof=1
	assert list(df['eventScoreDev']) == [-1.0, 0.0, 1.0, -1.0, 0.0, 1.0]


def test_per_scenario_constants_flow_into_computations(repo_root):
	cfg = read_config([
		str(repo_root / 'tests/fixtures/per_scenario_constants.yml'),
	])

	# the global config keeps the base constant; scenarios override per-key.
	assert get_computation_constants(cfg)['houseWeight'] == 1.0
	assert get_computation_constants(cfg['scenarios']['balanced'])['houseWeight'] == 1.0
	assert (
		get_computation_constants(cfg['scenarios']['houseHeavy'])['houseWeight']
		== 2.5
	)
	# minScore is inherited via deep-merge (not restated by the scenario).
	assert (
		get_computation_constants(cfg['scenarios']['houseHeavy'])['minScore']
		== 0
	)
	# the shared computation fields stay global; a scenario overriding one
	# constant does not have to restate them.
	assert (
		list(get_computation_fields(cfg['scenarios']['houseHeavy']).keys())
		== ['eventScore', 'eventScoreDev']
	)
	# report stays global and is not routed through scenario configs.
	assert cfg['report']['selection'] == (
		'eventScoreDev >= 1.0 and eventScore >= constants.minScore'
	)


def _combined_per_scenario_df(cfg):
	"""Reproduce the engine's per-scenario computation step without the
	global report projection, so computed columns can be inspected."""
	df = pd.DataFrame()
	for scenario_name in cfg['scenarios'].keys():
		scenario_df, scenario_config = generate_scenario_combos(
			scenario_name, cfg
		)
		add_custom_columns(
			scenario_df,
			get_computation_fields(scenario_config),
			scenario_config,
		)
		df = pd.concat([df, scenario_df], ignore_index=True)
	return df


def test_computations_apply_per_scenario_with_scenario_constants(repo_root):
	cfg = read_config([
		str(repo_root / 'tests/fixtures/per_scenario_constants.yml'),
	])
	df = _combined_per_scenario_df(cfg)

	# Pass 1: each scenario computes eventScore with its own houseWeight.
	# eventScore = h1 * houseWeight + h5 + h9  =>  (eventScore - h5 - h9) / h1.
	scenario_key = {'house-heavy': 'houseHeavy'}
	for scenario_name, group in df.groupby('scenario'):
		scenario_cfg = cfg['scenarios'][scenario_key.get(scenario_name, 'balanced')]
		weight = get_computation_constants(scenario_cfg)['houseWeight']
		ratio = (group['eventScore'] - group['h5'] - group['h9']) / group['h1']
		assert set(ratio.round(6).unique()) == {round(weight, 6)}, scenario_name

	# Pass 2: eventScoreDev is a per-scenario z-score (sample std, ddof=1).
	for scenario_name, group in df.groupby('scenario'):
		dev = group['eventScoreDev']
		assert abs(dev.mean()) < 1e-9, scenario_name
		# std of z-scores is 1 by construction (ddof=1).
		assert abs(dev.std(ddof=1) - 1.0) < 1e-9, scenario_name
		# the max row is the +1 sigma relative to its group mean/std.
		expected = (group['eventScore'] - group['eventScore'].mean()) / (
			group['eventScore'].std(ddof=1)
		)
		pd.testing.assert_series_equal(
			dev.reset_index(drop=True),
			expected.reset_index(drop=True),
			check_names=False,
		)


def test_generate_combos_keeps_report_global(repo_root):
	cfg = read_config([
		str(repo_root / 'tests/fixtures/per_scenario_constants.yml'),
	])
	out = generate_combos(cfg)

	# Pass 3: report.selection is applied once globally across the combined
	# DataFrame: every surviving row satisfies the selection predicate.
	pre = _combined_per_scenario_df(cfg)
	pre['minScore'] = 0
	survivors = pre.query(
		rewrite_constants_expression(
			'eventScoreDev >= 1.0 and eventScore >= constants.minScore'
		),
		local_dict=get_expression_locals(cfg),
	)
	assert set(out['scenario']) == set(survivors['scenario'])
	assert len(out) == len(survivors)

	# report.order is global: rows are sorted by eventScoreDev desc, then
	# eventScore desc across scenarios (not grouped by scenario first).
	devs = list(out['eventScoreDev'])
	assert devs == sorted(devs, reverse=True)

	# report.fieldSets is global: only the configured columns are emitted.
	# computations field-set surfaces eventScore / eventScoreDev explicitly.
	assert 'eventScore' in out.columns
	assert 'eventScoreDev' in out.columns
	assert 'h1' in out.columns  # ashtakavarga: all
	assert 'tithi' in out.columns  # panchang: all
	assert 'suD' not in out.columns  # planetaryDegrees not selected
