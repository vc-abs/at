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

	return df.query(config['query'])
