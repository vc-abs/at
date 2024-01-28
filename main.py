import sys
from pprint import pprint

from readConfig import readConfig
from chart import getObjects

def main(configFilePath="./sample.yml"):
	pprint(getObjects(readConfig(configFilePath)))

if __name__ == "__main__":
	main(*sys.argv[1:])
