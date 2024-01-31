import pandas as pd
from ashtakavarga import getAshtakavarga

def standardizeDate(dt):
	return {
		'year': dt.year,
		'month': dt.month,
		'date': dt.day,
		'hour': dt.hour,
		'minute': dt.minute,
		'second': dt.second,
	}

def getAshtakavargaForTime(config, dt):
	return {
		'time': dt,
		**getAshtakavarga({**config, **standardizeDate(dt) })
	}

def generateAshtakavarga(config):
	timeSeries = pd.date_range(
		start = config['date'],
		periods = config['periods'],
		freq=config['freq']
	).to_pydatetime().tolist()

	return pd.DataFrame(map(lambda dt: getAshtakavargaForTime(config, dt), timeSeries))
