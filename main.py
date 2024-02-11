import sys
from readWrite.output import output
from readWrite.readConfig import (
	readConfig,
)
from tools.generateCombos import (
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


if __name__ == '__main__':
	main(sys.argv[1:])
