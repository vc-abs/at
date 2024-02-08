import pandas as pd
from chart import Chart

orderMap = {
	'ascending': True,
	'descending': False,
}


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
	return {
		'time': dt,
		**chart.panchang.muhurtaYogaEffects,
		**chart.ashtakavarga,
	}


def addColumns(df, columns):
	keys = list(columns.keys())

	values = (
		pd.DataFrame(
			map(
				lambda exp: df.eval(exp),
				columns.values(),
			),
		)
		.transpose()
		.rename(
			columns={
				k: v for k, v in enumerate(keys)
			}
		)
	)
	df[keys] = values


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

	return df.query(config['query'])
