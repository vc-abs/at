from datetime import datetime, timezone

import pandas as pd

from at.tools.generateCombos import (
	addColumns,
	addCustomColumns,
	formatDashaData,
	getColumn,
	getPanchang,
	getPlanetaryDegrees,
	getPlanetFlagsByPlanet,
	getPlanetQualities,
	processSummaryColumn,
	sortData,
	splitTimestamp,
)


class _DummyPanchang:
	tithi = 1


class _DummyChart:
	def __init__(self, objects):
		self.objects = objects
		self.panchang = _DummyPanchang()


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
	assert getColumn(df, 'a + b').iloc[0] == 3
	assert getColumn(df, {'sum': ['a', 'b']}).iloc[0] == 3



def test_get_column_returns_unsupported_values_unchanged():
	df = pd.DataFrame([{'a': 1}])
	value = ['a']
	assert getColumn(df, value) is value



def test_process_summary_column_directly():
	df = pd.DataFrame(
		[
			{'x': 2, 'y': 3},
			{'x': 4, 'y': 5},
		]
	)
	res = processSummaryColumn(df, {'sum': ['x', 'y']})
	assert list(res) == [5, 9]



def test_add_custom_columns_adds_each_declared_column():
	df = pd.DataFrame([{'a': 1, 'b': 2}])
	addCustomColumns(
		df,
		{
			'c': 'a + b',
			'd': {'sum': ['a', 'b']},
		},
	)
	assert list(df.columns) == ['a', 'b', 'c', 'd']
	assert df['c'].iloc[0] == 3
	assert df['d'].iloc[0] == 3



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
