from os import makedirs, path
from io import StringIO
from pprint import pprint
from pandas import DataFrame


def exportToFile(context):
	exportTo = context['exportTo']
	makedirs(
		path.dirname(exportTo),
		exist_ok=True,
	)

	DataFrame(context['data']).to_csv(
		exportTo,
		index=False,
		sep=context['exportSeparator'],
	)


def printToStdOut(context):
	output = StringIO()

	DataFrame(context['data']).to_csv(
		output,
		index=False,
		sep=context['exportSeparator'],
	)

	print(output.getvalue(), end='')


def output(context):
	action = (
		exportToFile
		if context.get('exportTo')
		else printToStdOut
	)
	action(context)
