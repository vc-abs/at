import pandas as pd
from ashtakavarga import getAshtakavarga

columnRenameMap = {
	1: 'h1', 2: 'h2', 3: 'h3', 4: 'h4', 5: 'h5', 6: 'h6',
	7: 'h7', 8: 'h8', 9: 'h9', 10: 'h10', 11: 'h11', 12: 'h12',
}

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

	df = pd.DataFrame(
		list(map(lambda dt: getAshtakavargaForTime(config, dt), timeSeries)),
	).rename(columns=columnRenameMap)

	return df.query(config['query'])
