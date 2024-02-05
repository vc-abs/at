import pandas as pd
from chart import Chart


def standardizeDate(dt):
	return {
		'year': dt.year,
		'month': dt.month,
		'day': dt.day,
		'hour': dt.hour,
		'minute': dt.minute,
		'second': dt.second,
	}


def getComboForTime(config, dt):
	chart = Chart(
		{**config, **standardizeDate(dt)}
	)
	return {
		'time': dt,
		'muhurtaYogaEffect': chart.panchang.muhurtaYogaEffect,
		**chart.ashtakavarga,
	}


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

	columns = config['columns']
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

	return df.query(config['query'])
