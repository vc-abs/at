from functools import reduce
import pandas as pd
from chart import Chart

orderMap = {
	'ascending': True,
	'descending': False,
}


def getObjectHouses(chart):
	return dict(
		{
			'asS': chart.objects['asc'][
				'sign'
			]
		},
		**{
			(objectKey[:2] + 'H'): object[
				'house'
			]
			for (
				objectKey,
				object,
			) in chart.objects.items()
			if objectKey != 'asc'
		},
	)


placeHolderPlanetBalas = {
	'strength': 0,
	'ishtaPhala': 0,
}


def formatDashaData(
	dasha, balas, prefix
):
	dashaLordPhala = balas.get(
		dasha['lord'],
		placeHolderPlanetBalas,
	)

	return {
		**{
			f'{ prefix }{ k[0].upper() }{ k[1:] }': v
			for k, v in dasha.items()
		},
		f'{ prefix }lStrength': dashaLordPhala[
			'strength'
		],
		f'{ prefix }lIshtaPhala': dashaLordPhala[
			'ishtaPhala'
		],
	}


def getStartingDasha(chart):
	return formatDashaData(
		chart.dasha.startingDasha,
		chart.shadBala.balas,
		'sd',
	)


def getStartingAntarDashas(chart):
	formattedDashas = [
		formatDashaData(
			antarDashaData,
			chart.shadBala.balas,
			antarDashaPrefix,
		)
		for antarDashaPrefix, antarDashaData in chart.dasha.startingAntarDashas.items()
	]
	return {
		k: v
		for d in formattedDashas
		for k, v in d.items()
	}


phalaPlanetCount = 7


def getShadBalaStrength(chart):
	strengths = {
		planet: phala['strength']
		for planet, phala in chart.shadBala.balas.items()
	}

	avgIshtaPhala = (
		sum(
			phala['ishtaPhala']
			for phala in chart.shadBala.balas.values()
		)
		/ phalaPlanetCount
	)

	return {
		**{
			f'{planet[:2]}S': strength
			for planet, strength in strengths.items()
		},
		'totalS': sum(strengths.values()),
		'avgIP': avgIshtaPhala,
	}


def getKarakas(chart):
	return chart.karakas


fieldSets = {
	'muhurtaYogaEffects': lambda chart: chart.panchang.muhurtaYogaEffects,
	'objectHouses': getObjectHouses,
	'ashtakavarga': lambda chart: chart.ashtakavarga,
	'startingDasha': getStartingDasha,
	'startingAntarDashas': getStartingAntarDashas,
	'shadBalaStrength': getShadBalaStrength,
	'karakas': getKarakas,
}


def getFields(config, chart):
	return reduce(
		lambda acc, fieldSet: (
			{
				**acc,
				**fieldSets[fieldSet](chart),
			}
		),
		[{}] + config['fieldSets'],
	)


def standardizeDate(dt):
	return {
		'year': dt.year,
		'month': dt.month,
		'day': dt.day,
		'hour': dt.hour,
		'minute': dt.minute,
		'second': dt.second,
		'date': dt,
	}


def getTimeCombos(
	eventName, config, dt
):
	chart = Chart(
		{
			**config,
			**standardizeDate(dt),
			'datetime': dt,
		}
	)

	fields = getFields(config, chart)

	return {
		'timestamp': dt,
		'event': eventName,
		**fields,
	}


def generateEventCombos(
	eventName, config
):
	config = {
		**config,
		**config['events'][eventName],
	}
	timeSeries = (
		pd.date_range(
			start=config['date'],
			periods=config['periods'],
			freq=config['frequency'],
		)
		.to_pydatetime()
		.tolist()
	)

	return pd.DataFrame(
		list(
			map(
				lambda dt: getTimeCombos(
					eventName, config, dt
				),
				timeSeries,
			)
		),
	)


def processSummaryColumn(df, summary):
	summaryFn, summaryColumns = next(
		iter(summary.items())
	)

	return getattr(
		df[summaryColumns], summaryFn
	)(axis=1)


columnProcessors = {
	'str': lambda df, exp: df.eval(exp),
	'OrderedDict': processSummaryColumn,
}


def getType(value):
	return type(value).__name__


def getColumn(df, column):
	return columnProcessors[
		getType(column)
	](df, column)


def addCustomColumns(df, columns):
	keys = list(columns.keys())

	for key in keys:
		df[key] = getColumn(
			df, columns[key]
		)


def sortData(df, order):
	keys = list(order.keys())
	orders = list(
		map(
			lambda column: orderMap[column],
			order.values(),
		)
	)

	return df.sort_values(
		by=keys,
		ascending=orders,
		inplace=True,
	)


def splitTimestamp(df):
	df.insert(
		0,
		'date',
		df['timestamp'].map(
			lambda timestamp: timestamp.strftime(
				'%Y-%m-%d'
			)
		),
	)

	df.insert(
		1,
		'time',
		df['timestamp'].map(
			lambda timestamp: timestamp.strftime(
				'%H:%M:%S'
			)
		),
	)

	return df.drop(
		columns=['timestamp'], inplace=True
	)


def adjustColumns(df):
	eventColumn = df.pop('event')
	df.insert(0, 'event', eventColumn)


def skipColumns(df, columns):
	return df.drop(columns=columns)


def generateCombos(config):
	df = pd.DataFrame()

	for eventName in config[
		'events'
	].keys():
		df = pd.concat(
			[
				df,
				generateEventCombos(
					eventName, config
				),
			],
		)

	addCustomColumns(
		df, config['customColumns']
	)
	sortData(df, config['order'])
	splitTimestamp(df)
	adjustColumns(df)
	filteredDF = df.query(config['query'])
	modifiedDF = skipColumns(
		filteredDF, config['skipColumns']
	)

	return modifiedDF
