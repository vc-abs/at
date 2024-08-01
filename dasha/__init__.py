from datetime import timedelta
from core.Cached import Cached
from core.constants import (
	daysPerYear,
	nakshatraWidth,
)

vimshottariLengths = {
	'ketu': 7,
	'venus': 20,
	'sun': 6,
	'moon': 10,
	'mars': 7,
	'rahu': 18,
	'jupiter': 16,
	'saturn': 19,
	'mercury': 17,
}
vimshottariLengthsTotal = sum(
	vimshottariLengths.values()
)
vimshottariProportions = {
	planet: length
	/ vimshottariLengthsTotal
	for planet, length in vimshottariLengths.items()
}
vimshottariSequence = list(
	vimshottariLengths.keys()
)
dashaCount = len(vimshottariSequence)
nakshatraLordCount = len(
	vimshottariSequence
)

doubleCycle = (
	vimshottariSequence
	+ vimshottariSequence
)


def getNakshatraIndex(chart):
	return (
		chart.panchang.nakshatraNumber - 1
	)


antarDashaPrefixes = [
	'ad',
	'pad',
	'skd',
	'prd',
]
antarDashaMaxDepth = len(
	antarDashaPrefixes
)


def getAntarDasha(
	startingPlanet,
	superDashaStartsAt,
	superDashaLength,
	coveredFraction,
	currentAntarDashaDepth=0,
	requestedAntarDashaDepth=None,
):
	if requestedAntarDashaDepth is None:
		requestedAntarDashaDepth = (
			currentAntarDashaDepth
		)

	coveredLength = (
		coveredFraction * superDashaLength
	)
	accumulatedLength = 0
	currentAntarDashaLength = 0
	dashaPlanet = None
	sequenceStart = (
		vimshottariSequence.index(
			startingPlanet
		)
	)
	for currentPlanet in doubleCycle[
		sequenceStart:
	]:
		currentAntarDashaLength = (
			vimshottariProportions[
				currentPlanet
			]
			* superDashaLength
		)

		accumulatedLength += (
			currentAntarDashaLength
		)
		dashaPlanet = currentPlanet
		if (
			accumulatedLength >= coveredLength
		):
			break

	completedLength = (
		accumulatedLength
		- currentAntarDashaLength
	)
	startsAt = (
		superDashaStartsAt
		+ timedelta(
			days=completedLength * daysPerYear
		)
	)
	endsAt = (
		superDashaStartsAt
		+ timedelta(
			days=accumulatedLength
			* daysPerYear
		)
	)
	remainingFraction = (
		accumulatedLength - coveredLength
	) / currentAntarDashaLength
	antarDashaPrefix = antarDashaPrefixes[
		requestedAntarDashaDepth
		- currentAntarDashaDepth
	]
	dashaValues = {
		antarDashaPrefix: {
			'lord': dashaPlanet,
			'startsAt': startsAt,
			'endsAt': endsAt,
			'remainder': remainingFraction,
		}
	}

	subDashaValues = (
		getAntarDasha(
			dashaPlanet,
			startsAt,
			currentAntarDashaLength,
			1 - remainingFraction,
			currentAntarDashaDepth - 1,
			requestedAntarDashaDepth,
		)
		if currentAntarDashaDepth
		else {}
	)

	return {
		**dashaValues,
		**subDashaValues,
	}


class Dasha(Cached):
	def __init__(self, chart):
		super().__init__()
		self._chart = chart

	def _getNakshatraLord(self):
		return {
			'nakshatraLord': vimshottariSequence[
				getNakshatraIndex(self._chart)
				% nakshatraLordCount
			],
		}

	def _getDashas(self):
		startingDasha = (
			self._getStartingDasha()
		)
		startDate = startingDasha['endDate']
		dashaStartIndex = (
			vimshottariSequence.index(
				startingDasha['planet']
			)
		)

		dashas = [startingDasha]
		for i in range(1, dashaCount):
			planetIndex = (
				dashaStartIndex + i
			) % dashaCount
			planet = vimshottariSequence[
				planetIndex
			]
			dashaPeriodYears = (
				vimshottariLengths[planet]
			)

			endDate = startDate + timedelta(
				days=dashaPeriodYears
				* daysPerYear
			)
			dashas.append(
				{
					'lord': planet,
					'startsAt': startDate,
					'endsAt': endDate,
					'remainder': 1,
				}
			)

			startDate = endDate
		return dashas

	def _getStartingDasha(self):
		eventTime = self._chart.config[
			'datetime'
		]
		moonPosition = self._chart.objects[
			'moon'
		]['longitude']
		nakshatraIndex = getNakshatraIndex(
			self._chart
		)
		dashaStartIndex = (
			nakshatraIndex
			% nakshatraLordCount
		)
		startPlanet = vimshottariSequence[
			dashaStartIndex
		]
		nakshatraStartDegree = (
			nakshatraIndex * nakshatraWidth
		)
		coveredFraction = (
			moonPosition
			- nakshatraStartDegree
		) / nakshatraWidth
		remainingDashaPeriod = (
			1 - coveredFraction
		)
		dashaLength = vimshottariLengths[
			startPlanet
		]
		coveredLength = (
			dashaLength * coveredFraction
		)
		startsAt = eventTime - timedelta(
			days=coveredLength * daysPerYear
		)
		endsAt = startsAt + timedelta(
			days=dashaLength * daysPerYear
		)

		return {
			'lord': startPlanet,
			'startsAt': startsAt,
			'endsAt': endsAt,
			'remainder': remainingDashaPeriod,
		}

	def _getStartingAntarDashas(self):
		startingDasha = self.startingDasha
		coveredFraction = (
			1 - startingDasha['remainder']
		)
		return getAntarDasha(
			startingDasha['lord'],
			startingDasha['startsAt'],
			vimshottariLengths[
				startingDasha['lord']
			],
			coveredFraction,
			3,
		)
