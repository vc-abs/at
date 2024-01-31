import yaml
from datetime import datetime, timezone, timedelta

defaults = {
	"ayanamsa": "ay_raman",
	"hour": 0,
	"minute": 0,
	"second": 0,
	"year": 2024,
	"month": 1,
	"day": 1,
	"freq": '60min',
	"periods": 1000,
	# India specific defaults.
	"utcHour": 5,
	"utcMinute": 30,
	# Location of Delhi
	"latitude": 28.12,
	"longitude": 77,
	"query": "h1 > 1",
}

def readConfig(filePath):
	with open(filePath, "r") as stream:
		config = {**defaults, **yaml.safe_load(stream)}
		config['date'] = datetime(
			config['year'], config['month'], config['day'],
			config['hour'], config['minute'], config['second'], 000000,
			tzinfo=timezone(offset=timedelta(hours=config['utcHour'], minutes=config['utcMinute'])),
		)
		return config
