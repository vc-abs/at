import sys
from at.read_write.output import output
from at.read_write.read_config import (
	read_config,
)
from at.tools.generate_combos import (
	generate_combos,
)

default_config_file_paths = [
	'./examples/config.yml'
]


def main(
	input_config_file_paths,
):
	config_file_paths = (
		input_config_file_paths
		if len(input_config_file_paths)
		else default_config_file_paths
	)
	context = read_config(config_file_paths)
	data = generate_combos(context)
	output({'data': data, **context})


def cli():
	main(sys.argv[1:])


if __name__ == '__main__':
	cli()
