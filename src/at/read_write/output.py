from os import makedirs, path
from io import StringIO
from pandas import DataFrame


def export_to_file(context):
	export_to = context['exportTo']
	makedirs(
		path.dirname(export_to),
		exist_ok=True,
	)

	DataFrame(context['data']).to_csv(
		export_to,
		index=False,
		sep=context['exportSeparator'],
	)


def print_to_std_out(context):
	output = StringIO()

	DataFrame(context['data']).to_csv(
		output,
		index=False,
		sep=context['exportSeparator'],
	)

	print(output.getvalue(), end='')


def output(context):
	action = (
		export_to_file
		if context.get('exportTo')
		else print_to_std_out
	)
	action(context)
