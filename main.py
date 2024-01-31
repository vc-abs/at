import sys
from pprint import pprint

from readConfig import readConfig
from ashtakavarga import getAshtakavarga

def main(configFilePath="./sample.yml"):
	pprint(getAshtakavarga(readConfig(configFilePath)))

if __name__ == "__main__":
	main(*sys.argv[1:])
