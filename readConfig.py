import yaml

defaults = {
	"utcHour": 5,
	"utcMinute": 30,
}

def readConfig(filePath):
	with open(filePath, "r") as stream:
		return {**defaults, **yaml.safe_load(stream)}
