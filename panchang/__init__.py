import math
from core.Cached import Cached
from core.constants import (
	signCount,
	tithiCount,
	degrees,
	weekdays,
	daysInAWeek,
	weekdayLords,
	horaLordSequence,
	horasPerDay,
	nakshatras,
	nakshatraCount,
	padasPerNakshatra,
)
from core.sweHelpers import (
	getRiseAndSetTimes,
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

	def _getRiseAndSet(self):
		return getRiseAndSetTimes(
			self._chart._config
		)

	def _getDayLengths(self):
		riseAndSet = self.riseAndSet
		eventTime = self._chart.config[
			'datetime'
		]
		elapsed = int(
			(
				eventTime
				- riseAndSet['sunrise']
			).total_seconds()
		)
		length = int(
			(
				riseAndSet['nextRise']
				- riseAndSet['sunrise']
			).total_seconds()
		)

		return {
			'elapsed': elapsed,
			'total': length,
		}

	def _getTod(self):
		riseAndSetTimes = self.riseAndSet

		return (
			'day'
			if (
				riseAndSetTimes['sunrise']
				< self._chart.config['datetime']
				< riseAndSetTimes['sunset']
			)
			else 'night'
		)

	def _getVaara(self):
		calendarDayAdjustment = (
			self.riseAndSet['sunrise'].day
			- self._chart.config[
				'datetime'
			].day
		)

		return weekdays[
			(
				self._chart._config[
					'date'
				].weekday()
				+ 1
				+ calendarDayAdjustment
			)
			% daysInAWeek
		]

	def _getHora(self):
		vaara = self.vaara
		dayStartHoraLordIndex = (
			horaLordSequence.index(
				weekdayLords[vaara]
			)
		)
		eventHora = int(
			horasPerDay
			* (
				self.dayLengths['elapsed']
				/ self.dayLengths['total']
			)
		)
		eventHoraLordIndex = (
			dayStartHoraLordIndex + eventHora
		) % daysInAWeek

		return horaLordSequence[
			eventHoraLordIndex
		]

	def _getNakshatraNumber(self):
		return getOrdinalPosition(
			self._chart.objects['moon'][
				'longitude'
			],
			nakshatraCount,
		)

	def _getNakshatra(self):
		return nakshatras[
			self._getNakshatraNumber() - 1
		]

	def _getNakshatraPada(self):
		return (
			self._getNakshatraNumber() - 1
		) % padasPerNakshatra + 1

	def _getMuhurtaYogas(self):
		return getMuhurtaYogas(self)

	def _getMuhurtaYogaEffects(self):
		return getMuhurtaYogaEffects(self)
