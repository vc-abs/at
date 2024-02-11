from os import makedirs
from pprint import pprint
from pandas import DataFrame


def exportToFile(context):
	DataFrame(context['data']).to_csv(
		context['exportTo'],
		index=False,
		sep=context['exportSeparator'],
	)


def printToStdOut(context):
	pprint(context['data'])


def output(context):
	action = (
		exportToFile
		if context.get('exportTo')
		else printToStdOut
	)
	action(context)
