import sys
from at.readWrite.output import output
from at.readWrite.readConfig import (
	readConfig,
)
from at.tools.generateCombos import (
	generateCombos,
)

defaultConfigFilePaths = [
	'./examples/config.yml'
]


def main(
	inputConfigFilePaths,
):
	configFilePaths = (
		inputConfigFilePaths
		if len(inputConfigFilePaths)
		else defaultConfigFilePaths
	)
	context = readConfig(configFilePaths)
	data = generateCombos(context)
	output({'data': data, **context})


def cli():
	main(sys.argv[1:])


if __name__ == '__main__':
	cli()
