import sys
from output import output
from readConfig import readConfig
from tithi import getTithiDetails


def main(configFilePath='./sample.yml'):
	context = readConfig(configFilePath)
	data = getTithiDetails()
	output({'data': data, **context})


if __name__ == '__main__':
	main(*sys.argv[1:])
