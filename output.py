from pprint import pprint
from pandas import DataFrame


def output(context):
	exportFile = context.get('exportTo')
	data = context['data']

	if exportFile:
		DataFrame(data).to_csv(
			exportFile, index=False
		)
	else:
		pprint(data)
