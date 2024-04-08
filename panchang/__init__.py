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
from panchang.getMuhurtaYoga import (
	getMuhurtaYogas,
	getMuhurtaYogaEffects,
)


def getObjectDistance(
	source, destination
):
	return (
		destination['longitude']
		- source['longitude']
		+ degrees
	) % degrees


def hasSunRisen(chart):
	objects = chart.objects
	zeroHourAscendant = (
		chart.zeroHourChart.objects['asc']
	)
	return getObjectDistance(
		zeroHourAscendant, objects['asc']
	) >= getObjectDistance(
		zeroHourAscendant, objects['sun']
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

	def _getVaara(self):
		sunriseAdjustment = (
			0
			if hasSunRisen(self._chart)
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

	def _getMuhurtaYogas(self):
		return getMuhurtaYogas(self)

	def _getMuhurtaYogaEffects(self):
		return getMuhurtaYogaEffects(self)
