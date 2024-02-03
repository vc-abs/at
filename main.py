import sys
from output import output
from readConfig import readConfig
from chart import Chart


def main(configFilePath='./sample.yml'):
	context = readConfig(configFilePath)
	data = Chart(context).ashtakavarga
	output({'data': data, **context})


if __name__ == '__main__':
	main(*sys.argv[1:])
