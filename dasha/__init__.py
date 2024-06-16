from datetime import timedelta
from core.Cached import Cached
from core.constants import (
	daysPerYear,
	nakshatraWidth,
)

vimshottariDashaLength = {
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
nakshatraLordCount = len(
	vimshottariSequence
)


class Dasha(Cached):
	def __init__(self, chart):
		super().__init__()
		self._chart = chart

	def _getNakshatraIndex(self):
		return (
			self._chart.panchang.nakshatraNumber
			- 1
		)

	def _getNakshatraLord(self):
		return {
			'nakshatraLord': vimshottariSequence[
				self._getNakshatraIndex()
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
		for i in range(
			1, len(vimshottariSequence)
		):
			planetIndex = (
				dashaStartIndex + i
			) % len(vimshottariSequence)
			planet = vimshottariSequence[
				planetIndex
			]
			dashaPeriodYears = (
				vimshottariDashaLength[planet]
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
		chartTime = self._chart.config[
			'datetime'
		]
		moonPosition = self._chart.objects[
			'moon'
		]['longitude']
		nakshatraIndex = (
			self._getNakshatraIndex()
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
		nakshatraFraction = (
			moonPosition
			- nakshatraStartDegree
		) / nakshatraWidth
		remainingFraction = (
			1 - nakshatraFraction
		)

		startDate = chartTime
		remainingDashaYears = (
			vimshottariDashaLength[
				startPlanet
			]
			* remainingFraction
		)
		endDate = startDate + timedelta(
			days=remainingDashaYears
			* daysPerYear
		)

		return {
			'planet': startPlanet,
			'startDate': startDate,
			'endDate': endDate,
			'remainder': remainingFraction,
		}
