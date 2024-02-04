import math
from core.Cached import Cached
from core.constants import (
	signCount,
	tithiCount,
	degrees,
	weekDays,
	daysInAWeek,
	nakshatras,
	nakshatraCount,
	padaCount,
	padasPerNakshatra,
)
from core.helpers import (
	getOrdinalPosition,
)


def hasSunRisen(objects):
	return (
		objects['sun']['longitude']
		<= objects['asc']['longitude']
	)


class Panchang(Cached):
	def __init__(self, chart):
		super().__init__()
		self._chart = chart

	def _getTithi(self):
		return (
			math.ceil(
				(
					self._chart.objects['moon'][
						'longitude'
					]
					- self._chart.objects['sun'][
						'longitude'
					]
					+ degrees
				)
				% degrees
				/ signCount
			)
			% tithiCount
		)

	def _getVaar(self):
		sunriseAdjustment = (
			0
			if hasSunRisen(
				self._chart.objects
			)
			else -1
		)

		return weekDays[
			(
				self._chart._config[
					'date'
				].weekday()
				+ 1
				+ sunriseAdjustment
			)
			% daysInAWeek
		]

	def _getNakshatra(self):
		return nakshatras[
			getOrdinalPosition(
				self._chart.objects['moon'][
					'longitude'
				],
				nakshatraCount,
			)
			- 1
		]

	def _getNakshatraPada(self):
		return (
			getOrdinalPosition(
				self._chart.objects['moon'][
					'longitude'
				],
				padaCount,
			)
			- 1
		) % padasPerNakshatra + 1
