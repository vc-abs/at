import sys
from pprint import pprint

from readConfig import readConfig

def main(configFilePath="./sample.yml"):
	pprint(readConfig(configFilePath))

if __name__ == "__main__":
	main(*sys.argv[1:])
