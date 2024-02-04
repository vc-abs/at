import sys
from readWrite.output import output
from readWrite.readConfig import (
	readConfig,
)
from chart import Chart


def main(
	configFilePath='./examples/config.yml',
):
	context = readConfig(configFilePath)
	chart = Chart(context)
	data = chart.panchang._chart.tithi
	output({'data': data, **context})


if __name__ == '__main__':
	main(*sys.argv[1:])
