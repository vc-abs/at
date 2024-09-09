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

def getPanchang(chart):
	return {
		'tithi': chart.panchang.tithi,
		'nakshatra': chart.panchang.nakshatra,
		'vaara': chart.panchang.vaara
	}

fieldSets = {
	'muhurtaYogaEffects': {
  	'fn': lambda chart: chart.panchang.muhurtaYogaEffects,
  	'columns': ['positive', 'negative', 'yogas']
	},
	'objectHouses': {
		'fn': getObjectHouses,
		'columns': ['asS','suH', 'moH', 'maH', 'meH', 'juH', 'veH', 'saH', 'raH', 'keH']
	},
	'ashtakavarga': {
  	'fn': lambda chart: chart.ashtakavarga,
		'columns': ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12']
	},
	'startingDasha': {
		'fn': getStartingDasha,
		'columns': ['sdLord', 'sdStartsAt', 'sdEndsAt', 'sdRemainder', 'sdlStrength', 'sdlIshtaPhala']
	},
	'startingAntarDashas': {
  	'fn': getStartingAntarDashas,
		'columns': ['adLord', 'adStartsAt', 'adEndsAt', 'adRemainder', 'adlStrength', 'adlIshtaPhala', 'padLord', 'padStartsAt', 'padEndsAt', 'padRemainder', 'padlStrength', 'padlIshtaPhala', 'skdLord', 'skdStartsAt', 'skdEndsAt', 'skdRemainder', 'skdlStrength', 'skdlIshtaPhala','prdLord', 'prdStartsAt', 'prdEndsAt', 'prdRemainder', 'prdlStrength', 'prdlIshtaPhala']
	},
	'shadBalaStrength': {
  	'fn': getShadBalaStrength,
  	'columns': ['suS', 'moS', 'maS', 'maS', 'meS', 'juS', 'veS', 'saS', 'totalS', 'avgIP']
	},
	'karakas': {
  	'fn': getKarakas,
  	'columns': ['ak', 'amk', 'bk', 'mk', 'pk', 'gk', 'dk']
	},
	'event': {
		'fn': lambda chart: {},
		'columns': ['event', 'date', 'time']
	},
	'panchang': {
		'fn': getPanchang,
		'columns': ['tithi', 'nakshatra', 'vaara']
	}
}

def getFields(config, chart):
	return reduce(
		lambda acc, fieldSet: (
			{
				**acc,
				**fieldSets[fieldSet[0]]['fn'](chart),
			}
		),
		config['fieldSets'].items(), {}
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

selectionTypes = {
	'all': lambda key, columns : fieldSets[key]['columns'],
	'none': lambda key, columns : [],
	'some': lambda key, columns : columns
}

def addColumns(df, configFieldSets):
	columnsToInclude = []
	for fieldSet in configFieldSets.items():
		key, value = fieldSet
		selectorType = value if type(value).__name__ == 'str' else 'some'
		columnsToInclude = columnsToInclude + selectionTypes[selectorType](key, value)
	return df[columnsToInclude]

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
	modifiedDF = addColumns(
		filteredDF, config['fieldSets']
	)

	return modifiedDF
