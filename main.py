import sys
from pprint import pprint

from readConfig import readConfig
from chart import getChart, getObjects

def main(configFilePath="./sample.yml"):
	chart = getChart(**readConfig(configFilePath))
	pprint(getObjects(chart))

if __name__ == "__main__":
	main(*sys.argv[1:])
