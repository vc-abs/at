import pandas as pd

from at.tools.generateCombos import (
	addColumns,
	getPlanetaryDegrees,
	getPlanetFlagsByPlanet,
)


class _DummyChart:
	def __init__(self, objects):
		self.objects = objects


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
			'shadBalaStrength': ['avgIP'],
		},
	)

	assert list(selected.columns) == [
		'event',
		'date',
		'time',
		'asD',
		'suD',
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
