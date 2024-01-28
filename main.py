import sys
from pprint import pprint

from readConfig import readConfig
from getChart import getChart

def main(configFilePath="./sample.yml"):
	pprint(getChart(**readConfig(configFilePath)))

if __name__ == "__main__":
	main(*sys.argv[1:])
