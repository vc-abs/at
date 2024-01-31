import sys
from pprint import pprint

from readConfig import readConfig
from generateAshtakavarga import generateAshtakavarga

def main(configFilePath="./sample.yml"):
	pprint(generateAshtakavarga(readConfig(configFilePath)))

if __name__ == "__main__":
	main(*sys.argv[1:])
