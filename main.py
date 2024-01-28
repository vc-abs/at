import sys
from pprint import pprint

from readConfig import readConfig
from chart import getChart

def main(configFilePath="./sample.yml"):
	pprint(getChart(**readConfig(configFilePath)))

if __name__ == "__main__":
	main(*sys.argv[1:])
