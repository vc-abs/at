from collections.abc import Mapping
from functools import reduce
import pandas as pd
from at.chart import Chart
from at.core.constants import (
	planets,
	nodes,
	combustionOrbs,
)
from at.core.helpers import getShortestDistanceInCircle
from at.core.planetQuality import getPlanetQuality

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


def getPlanetaryDegrees(chart):
	return {
		'asD': chart.objects['asc'][
			'longitude'
		],
		**{
			f'{planet[:2]}D': chart.objects[planet][
				'longitude'
			]
			for planet in planets
		},
		**{
			f'{node[:2]}D': chart.objects[node][
				'longitude'
			]
			for node in nodes
		},
	}


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


def getMahaDasha(chart):
	return formatDashaData(
		chart.dasha.mahaDasha,
		chart.shadBala.balas,
		'md',
	)


def getAntarDashas(chart):
	formattedDashas = [
		formatDashaData(
			antarDashaData,
			chart.shadBala.balas,
			antarDashaPrefix,
		)
		for antarDashaPrefix, antarDashaData in chart.dasha.antarDashas.items()
	]
	return {
		k: v
		for d in formattedDashas
		for k, v in d.items()
	}


def getPlanetFlagsByPlanet(chart, planet):
	sunLongitude = chart.objects['sun']['longitude']
	planetData = chart.objects[planet]
	flags = []

	if planetData.get('retrograde'):
		flags.append('R')

	combustionOrb = combustionOrbs.get(planet)
	if combustionOrb and (
		getShortestDistanceInCircle(
			planetData['longitude'],
			sunLongitude,
		)
		<= combustionOrb
	):
		flags.append('C')

	return '|'.join(sorted(flags))


def getPlanetFlags(chart):
	return {
		f'{planet[:2]}F': getPlanetFlagsByPlanet(
			chart, planet
		)
		for planet in planets
	}


def getPlanetQualities(chart):
	return {
		f'{planet[:2]}Q': getPlanetQuality(
			chart.objects[planet], chart
		)
		for planet in planets
	}


timeFlagSegmentsByVaara = {
	'sunday': {'RK': 8, 'YG': 5, 'GK': 7},
	'monday': {'RK': 2, 'YG': 4, 'GK': 6},
	'tuesday': {'RK': 7, 'YG': 3, 'GK': 5},
	'wednesday': {'RK': 5, 'YG': 2, 'GK': 4},
	'thursday': {'RK': 6, 'YG': 1, 'GK': 3},
	'friday': {'RK': 4, 'YG': 7, 'GK': 2},
	'saturday': {'RK': 3, 'YG': 6, 'GK': 1},
}


def isWithinDaySegment(
	eventTime,
	segmentIndex,
	dayStart,
	dayEnd,
	segmentCount=8,
):
	if not dayStart <= eventTime < dayEnd:
		return False

	segmentDuration = (
		dayEnd - dayStart
	) / segmentCount
	segmentStart = dayStart + (
		segmentDuration * (segmentIndex - 1)
	)
	segmentEnd = dayStart + (
		segmentDuration * segmentIndex
	)

	return segmentStart <= eventTime < segmentEnd



def getTimeFlags(chart):
	riseAndSet = chart.panchang.riseAndSet
	eventTime = chart.config['datetime']
	dayStart = riseAndSet['sunrise']
	dayEnd = riseAndSet['sunset']
	flagSegments = timeFlagSegmentsByVaara[
		chart.panchang.vaara
	]
	flags = [
		flag
		for flag, segmentIndex in flagSegments.items()
		if isWithinDaySegment(
			eventTime,
			segmentIndex,
			dayStart,
			dayEnd,
		)
	]

	return {
		'timeF': '|'.join(sorted(flags))
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
	riseAndSet = chart.panchang.riseAndSet
	sunrise = riseAndSet['sunrise'].strftime("%H:%M:%S")
	sunset = riseAndSet['sunset'].strftime("%H:%M:%S")

	return {
		'tithi': chart.panchang.tithi,
		'nakshatra': chart.panchang.nakshatra,
		'vaara': chart.panchang.vaara,
		'sunrise': sunrise,
		'sunset': sunset,
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
	'planetaryDegrees': {
		'fn': getPlanetaryDegrees,
		'columns': ['asD', 'suD', 'moD', 'maD', 'meD', 'juD', 'veD', 'saD', 'raD', 'keD']
	},
	'ashtakavarga': {
		'fn': lambda chart: chart.ashtakavarga,
		'columns': ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12']
	},
	'mahaDasha': {
		'fn': getMahaDasha,
		'columns': ['mdLord', 'mdStartsAt', 'mdEndsAt', 'mdRemainder', 'mdlStrength', 'mdlIshtaPhala']
	},
	'antarDashas': {
		'fn': getAntarDashas,
		'columns': ['adLord', 'adStartsAt', 'adEndsAt', 'adRemainder', 'adlStrength', 'adlIshtaPhala', 'padLord', 'padStartsAt', 'padEndsAt', 'padRemainder', 'padlStrength', 'padlIshtaPhala', 'skdLord', 'skdStartsAt', 'skdEndsAt', 'skdRemainder', 'skdlStrength', 'skdlIshtaPhala','prdLord', 'prdStartsAt', 'prdEndsAt', 'prdRemainder', 'prdlStrength', 'prdlIshtaPhala']
	},
	'planetFlags': {
		'fn': getPlanetFlags,
		'columns': ['suF', 'moF', 'maF', 'meF', 'juF', 'veF', 'saF']
	},
	'planetQualities': {
		'fn': getPlanetQualities,
		'columns': ['suQ', 'moQ', 'maQ', 'meQ', 'juQ', 'veQ', 'saQ']
	},
	'timeFlags': {
		'fn': getTimeFlags,
		'columns': ['timeF']
	},
	'shadBalaStrength': {
		'fn': getShadBalaStrength,
		'columns': ['suS', 'moS', 'maS', 'meS', 'juS', 'veS', 'saS', 'totalS', 'avgIP']
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
		'columns': ['tithi', 'nakshatra', 'vaara', 'sunrise', 'sunset']
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
	eventConfig = config['events'][eventName]
	config = {
		**config,
		**eventConfig,
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
					eventConfig.get('name', eventName), config, dt
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


def getColumn(df, column):
	if isinstance(column, str):
		return df.eval(column)

	if isinstance(column, Mapping):
		return processSummaryColumn(df, column)

	return column


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
