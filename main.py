import sys
from pprint import pprint

from readConfig import readConfig
from generateAshtakavarga import generateAshtakavarga

def output(context):
	exportFile = context.get('exportTo')
	df = context['df']

	if exportFile:
		df.to_csv(exportFile)
	else:
		pprint(df)

def main(configFilePath="./sample.yml"):
	context = readConfig(configFilePath)
	df = generateAshtakavarga(context)
	output({'df': df, **context})

if __name__ == "__main__":
	main(*sys.argv[1:])
