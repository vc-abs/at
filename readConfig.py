import yaml

defaults = {
	"ayanamsa": "ay_raman",
	"hour": 0,
	"minute": 0,
	"second": 0,
	"year": 2024,
	"month": 1,
	"day": 1,
	# India specific defaults.
	"utcHour": 5,
	"utcMinute": 30,
	# Location of Delhi
	"latitude": 28.12,
	"longitude": 77,
}

def readConfig(filePath):
	with open(filePath, "r") as stream:
		return {**defaults, **yaml.safe_load(stream)}
