from pprint import pprint
from pandas import DataFrame


def output(context):
	exportTo = context.get('exportTo')
	exportSeparator = context[
		'exportSeparator'
	]
	data = context['data']

	if exportTo:
		DataFrame(data).to_csv(
			exportTo,
			index=False,
			sep=exportSeparator,
		)
	else:
		pprint(data)
