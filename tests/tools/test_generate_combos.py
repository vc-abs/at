from datetime import datetime, timezone

import pandas as pd

from at.tools.generateCombos import (
	addColumns,
	addCustomColumns,
	formatDashaData,
	getColumn,
	getExpressionLocals,
	getGowriFlags,
	getPanchang,
	getPlanetaryDegrees,
	getPlanetFlagsByPlanet,
	getPlanetQualities,
	getTimeFlags,
	processSummaryColumn,
	resolveConstantReference,
	rewriteConstantsExpression,
	sortData,
	splitTimestamp,
)


class _DummyPanchang:
	def __init__(self):
		self.tithi = 1
		self.vaara = 'wednesday'
		self.riseAndSet = {
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


class _DummyChart:
	def __init__(self, objects, event_time=None):
		self.objects = objects
		self.panchang = _DummyPanchang()
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


class _PanchangObj:
	def __init__(self):
		self.riseAndSet = {
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


class _PanchangChart:
	def __init__(self):
		self.panchang = _PanchangObj()



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
	chart = _DummyChart(_chart_objects_for_flags())

	# mercury: retrograde + within 14 degrees of sun -> C|R
	assert getPlanetFlagsByPlanet(chart, 'mercury') == 'C|R'
	# moon: combust only
	assert getPlanetFlagsByPlanet(chart, 'moon') == 'C'
	# jupiter: retro only (too far from sun)
	assert getPlanetFlagsByPlanet(chart, 'jupiter') == 'R'



def test_planetary_degrees_include_asc_and_nodes_in_order():
	chart = _DummyChart(_chart_objects_for_flags())
	degrees = getPlanetaryDegrees(chart)

	keys = list(degrees.keys())
	assert keys[0] == 'asD'
	assert keys[-2:] == ['raD', 'keD']
	assert degrees['asD'] == 100.0
	assert degrees['raD'] == 220.0
	assert degrees['keD'] == 40.0



def test_planet_qualities_include_all_planets_with_expected_values():
	chart = _DummyChart(_chart_objects_for_flags())
	qualities = getPlanetQualities(chart)

	assert qualities['suQ'] == 'malefic'
	assert qualities['moQ'] == 'malefic'
	assert qualities['maQ'] == 'malefic'
	assert qualities['meQ'] == 'malefic'
	assert qualities['juQ'] == 'benefic'
	assert qualities['veQ'] == 'benefic'
	assert qualities['saQ'] == 'malefic'



def test_time_flags_encode_active_day_segment_markers():
	chart = _DummyChart(
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
	flags = getTimeFlags(chart)

	assert flags['timeF'] == 'RK'



def test_time_flags_are_empty_outside_marked_segments():
	chart = _DummyChart(
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
	flags = getTimeFlags(chart)

	assert flags['timeF'] == ''



def test_format_dasha_data_uses_placeholder_when_bala_missing():
	dasha = {
		'lord': 'rahu',
		'startsAt': datetime(2025, 1, 1, tzinfo=timezone.utc),
		'endsAt': datetime(2026, 1, 1, tzinfo=timezone.utc),
		'remainder': 0.5,
	}
	balas = {}
	out = formatDashaData(dasha, balas, 'md')

	assert out['mdLord'] == 'rahu'
	assert out['mdlStrength'] == 0
	assert out['mdlIshtaPhala'] == 0



def test_get_column_supports_str_expression_and_dict_summary():
	df = pd.DataFrame([{'a': 1, 'b': 2}])
	config = {'constants': {}}
	assert getColumn(df, 'a + b', config).iloc[0] == 3
	assert getColumn(df, {'sum': ['a', 'b']}, config).iloc[0] == 3



def test_get_column_returns_unsupported_values_unchanged():
	df = pd.DataFrame([{'a': 1}])
	value = ['a']
	assert getColumn(df, value, {'constants': {}}) is value



def test_process_summary_column_directly():
	df = pd.DataFrame(
		[
			{'x': 2, 'y': 3},
			{'x': 4, 'y': 5},
		]
	)
	res = processSummaryColumn(
		df,
		{'sum': ['x', 'y']},
		{'constants': {}},
	)
	assert list(res) == [5, 9]



def test_add_custom_columns_adds_each_declared_column():
	df = pd.DataFrame([{'a': 1, 'b': 2}])
	addCustomColumns(
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
	assert rewriteConstantsExpression(
		'vaara.isin(constants.marketingWeekdays)'
	) == 'vaara.isin(@constants.marketingWeekdays)'
	assert rewriteConstantsExpression(
		'constants.thresholds.score >= 300'
	) == '@constants.thresholds.score >= 300'
	assert rewriteConstantsExpression(
		'vaara.isin(@constants.marketingWeekdays)'
	) == 'vaara.isin(@constants.marketingWeekdays)'



def test_get_expression_locals_exposes_constants_namespace():
	locals_ = getExpressionLocals(
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
	locals_ = getExpressionLocals(
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
	result = getColumn(
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
	res = processSummaryColumn(
		df,
		{'min': 'constants.marketingMinHouses'},
		config,
	)
	assert list(res) == [22, 26]



def test_resolve_constant_reference_returns_non_constant_strings_unchanged():
	config = {'constants': {'x': ['a']}}
	assert resolveConstantReference(['h1'], config) == ['h1']
	assert resolveConstantReference('h1', config) == 'h1'



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
	addCustomColumns(
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
	addCustomColumns(
		df,
		{
			'weekdayScore': (
				'vaara.map(constants.marketingWeekdayWeights).fillna(0)'
			),
		},
		config,
	)
	assert list(df['weekdayScore']) == [30.0, 24.0, 0.0]



def test_launch_preset_uses_constants_pattern_consistently():
	with open('presets/launch.yml', 'r') as f:
		text = f.read()

	assert 'constants:' in text
	assert 'launchWeekdayWeights:' in text
	assert 'launchCorePlanets:' in text
	assert 'vaara.map(constants.launchWeekdayWeights).fillna(0)' in text
	assert 'mdLord.isin(constants.launchCorePlanets)' in text
	assert 'min: constants.launchMinHouses' in text



def test_staff_onboarding_preset_uses_constants_pattern_consistently():
	with open('presets/staffOnboarding.yml', 'r') as f:
		text = f.read()

	assert 'constants:' in text
	assert 'staffOnboardingWeekdayWeights:' in text
	assert 'staffOnboardingCorePlanets:' in text
	assert 'vaara.map(constants.staffOnboardingWeekdayWeights).fillna(0)' in text
	assert 'mdLord.isin(constants.staffOnboardingCorePlanets)' in text
	assert 'min: constants.staffOnboardingMinHouses' in text



def test_student_onboarding_preset_uses_constants_pattern_consistently():
	with open('presets/studentOnboarding.yml', 'r') as f:
		text = f.read()

	assert 'constants:' in text
	assert 'studentOnboardingWeekdayWeights:' in text
	assert 'studentOnboardingCorePlanets:' in text
	assert 'vaara.map(constants.studentOnboardingWeekdayWeights).fillna(0)' in text
	assert 'mdLord.isin(constants.studentOnboardingCorePlanets)' in text
	assert 'min: constants.studentOnboardingMinHouses' in text



def test_sort_data_and_split_timestamp_mutate_dataframe():
	df = pd.DataFrame(
		[
			{
				'event': 'e',
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
				'event': 'e',
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

	sortData(df, {'score': 'descending'})
	assert list(df['score']) == [2, 1]

	splitTimestamp(df)
	assert 'timestamp' not in df.columns
	assert list(df.columns[:2]) == ['date', 'time']



def test_get_panchang_formats_time_strings():
	result = getPanchang(_PanchangChart())
	assert result['sunrise'] == '06:00:00'
	assert result['sunset'] == '18:00:00'
	assert result['tithi'] == 1
	assert result['gowri'] == 'laabam'
	assert result['gowriStart'] == '06:00:00'
	assert result['gowriScore'] == 1



def test_get_gowri_flags_formats_compact_fields():
	result = getGowriFlags(_PanchangChart())
	assert result['gowri'] == 'laabam'
	assert result['gowriScore'] == 1
	assert result['gowriStart'] == '06:00:00'
	assert result['gowriEnd'] == '07:30:00'
	assert result['gowriF'] == 'day|laabam'



def test_add_columns_supports_all_none_and_some_selectors():
	df = pd.DataFrame(
		[
			{
				'event': 'default',
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

	selected = addColumns(
		df,
		{
			'event': 'all',
			'planetaryDegrees': ['asD', 'suD'],
			'planetFlags': 'none',
			'planetQualities': ['suQ'],
			'timeFlags': ['timeF'],
			'gowriFlags': ['gowri', 'gowriScore', 'gowriF'],
			'shadBalaStrength': ['avgIP'],
		},
	)

	assert list(selected.columns) == [
		'event',
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
				'event': 'e',
				'date': '2025-01-01',
				'time': '00:00:00',
				'suF': 'C',
				'moF': '',
				'asD': 1.0,
				'suD': 2.0,
			}
		]
	)

	selected = addColumns(
		df,
		{
			'planetFlags': ['suF', 'moF'],
			'planetaryDegrees': ['asD', 'suD'],
		},
	)

	assert list(selected.columns) == ['suF', 'moF', 'asD', 'suD']
