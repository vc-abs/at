import sys
from readConfig import readConfig

def main(configFilePath="./sample.yml"):
  print(readConfig(configFilePath))

if __name__ == "__main__":
	main(*sys.argv[1:])
