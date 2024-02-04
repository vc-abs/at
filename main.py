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
	panchang = Chart(context).panchang
	data = panchang.muhurtaYoga
	output({'data': data, **context})


if __name__ == '__main__':
	main(*sys.argv[1:])
