from functools import reduce
import pandas as pd
from chart import Chart

orderMap = {
	'ascending': True,
	'descending': False,
}


def getObjectHouses(chart):
	return dict(
		{
			'asS': chart.objects['asc'][
				'sign'
			]
		},
		**{
			(objectKey[:2] + 'H'): object[
				'house'
			]
			for (
				objectKey,
				object,
			) in chart.objects.items()
			if objectKey != 'asc'
		},
	)


fieldSets = {
	'muhurtaYogaEffects': lambda chart: chart.panchang.muhurtaYogaEffects,
	'objectHouses': getObjectHouses,
	'ashtakavarga': lambda chart: chart.ashtakavarga,
}


def getFields(config, chart):
	return reduce(
		lambda acc, fieldSet: (
			{
				**acc,
				**fieldSets[fieldSet](chart),
			}
		),
		[{}] + config['fieldSets'],
	)


def standardizeDate(dt):
	return {
		'year': dt.year,
		'month': dt.month,
		'day': dt.day,
		'hour': dt.hour,
		'minute': dt.minute,
		'second': dt.second,
		'date': dt,
	}


def getComboForTime(config, dt):
	chart = Chart(
		{**config, **standardizeDate(dt)}
	)

	fields = getFields(config, chart)

	return {
		'timestamp': dt,
		**fields,
	}


def processSummaryColumn(df, summary):
	summaryFn, summaryColumns = next(
		iter(summary.items())
	)

	return getattr(
		df[summaryColumns], summaryFn
	)(axis=1)


columnProcessors = {
	'str': lambda df, exp: df.eval(exp),
	'OrderedDict': processSummaryColumn,
}


def getType(value):
	return type(value).__name__


def getColumn(df, column):
	return columnProcessors[
		getType(column)
	](df, column)


def addColumns(df, columns):
	keys = list(columns.keys())

	for key in keys:
		df[key] = getColumn(
			df, columns[key]
		)


def sortData(df, order):
	keys = list(order.keys())
	orders = list(
		map(
			lambda column: orderMap[column],
			order.values(),
		)
	)

	return df.sort_values(
		by=keys,
		ascending=orders,
		inplace=True,
	)


def splitTimestamp(df):
	df.insert(
		0,
		'date',
		df['timestamp'].map(
			lambda timestamp: timestamp.strftime(
				'%Y-%m-%d'
			)
		),
	)

	df.insert(
		1,
		'time',
		df['timestamp'].map(
			lambda timestamp: timestamp.strftime(
				'%H:%M:%S'
			)
		),
	)

	return df.drop(
		columns=['timestamp'], inplace=True
	)


def generateCombos(config):
	timeSeries = (
		pd.date_range(
			start=config['date'],
			periods=config['periods'],
			freq=config['freq'],
		)
		.to_pydatetime()
		.tolist()
	)

	df = pd.DataFrame(
		list(
			map(
				lambda dt: getComboForTime(
					config, dt
				),
				timeSeries,
			)
		),
	)

	addColumns(df, config['columns'])
	sortData(df, config['order'])
	splitTimestamp(df)

	return df.query(config['query'])
