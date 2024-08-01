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
					'planet': planet,
					'startDate': startDate,
					'endDate': endDate,
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
		coveredDashaPeriod = (
			moonPosition
			- nakshatraStartDegree
		) / nakshatraWidth
		remainingDashaPeriod = (
			1 - coveredDashaPeriod
		)
		dashaLength = vimshottariLengths[
			startPlanet
		]
		coveredDashaYears = (
			dashaLength * coveredDashaPeriod
		)
		startsAt = eventTime - timedelta(
			days=coveredDashaYears
			* daysPerYear
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
