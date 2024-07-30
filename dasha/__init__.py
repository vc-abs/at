from datetime import timedelta
from core.Cached import Cached
from core.constants import (
	daysPerYear,
	nakshatraWidth,
)

vimshottariDashaLengths = {
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
vimshottariDashaTotalLength = sum(
	vimshottariDashaLengths.values()
)
vimshottariSequence = [
	'ketu',
	'venus',
	'sun',
	'moon',
	'mars',
	'rahu',
	'jupiter',
	'saturn',
	'mercury',
]
dashaCount = len(vimshottariSequence)
nakshatraLordCount = len(
	vimshottariSequence
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
				vimshottariDashaLengths[planet]
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
		dashaLength = (
			vimshottariDashaLengths[
				startPlanet
			]
		)
		coveredDashaYears = (
			dashaLength * coveredDashaPeriod
		)
		startDate = eventTime - timedelta(
			days=coveredDashaYears
			* daysPerYear
		)
		endDate = startDate + timedelta(
			days=dashaLength * daysPerYear
		)

		return {
			'planet': startPlanet,
			'startDate': startDate,
			'endDate': endDate,
			'remainder': remainingDashaPeriod,
		}
