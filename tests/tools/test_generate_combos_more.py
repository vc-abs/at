from datetime import datetime, timezone

import pandas as pd

from at.tools.generateCombos import (
	addCustomColumns,
	formatDashaData,
	getColumn,
	getPanchang,
	processSummaryColumn,
	sortData,
	splitTimestamp,
)


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


class _Chart:
	def __init__(self):
		self.panchang = _PanchangObj()


def test_get_panchang_formats_time_strings():
	result = getPanchang(_Chart())
	assert result['sunrise'] == '06:00:00'
	assert result['sunset'] == '18:00:00'
	assert result['tithi'] == 1
