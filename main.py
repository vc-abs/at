import sys
from output import output

from readConfig import readConfig
from generateAshtakavarga import generateAshtakavarga

def main(configFilePath='./sample.yml'):
	context = readConfig(configFilePath)
	data = generateAshtakavarga(context)
	output({'data': data, **context})

if __name__ == '__main__':
	main(*sys.argv[1:])
