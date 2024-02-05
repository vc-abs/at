import sys
from readWrite.output import output
from readWrite.readConfig import (
	readConfig,
)
from tools.generateCombos import (
	generateCombos,
)


def main(
	configFilePath='./examples/config.yml',
):
	context = readConfig(configFilePath)
	data = generateCombos(context)
	output({'data': data, **context})


if __name__ == '__main__':
	main(*sys.argv[1:])
