import math
from datetime import (
	datetime,
	time,
	timezone,
)
from core.Cached import Cached
from core.constants import (
	signCount,
	tithiCount,
	degrees,
	weekdays,
	daysInAWeek,
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


def hasSunRisen(
	config, riseAndSetTimes
):
	return (
		config['datetime']
		>= riseAndSetTimes['sunrise']
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

	def _getRiseAndSet(self):
		return getRiseAndSetTimes(
			self._chart._config
		)

	def _getDayLengths(self):
		riseAndSet = self.riseAndSet
		eventTime = self._chart.config[
			'datetime'
		]

		dayStart = datetime.combine(
			eventTime.date(), time.min
		).replace(tzinfo=timezone.utc)

		elapsed = (
			eventTime - dayStart
		).total_seconds()
		length = (
			riseAndSet['nextRise']
			- riseAndSet['sunrise']
		).total_seconds()

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
		sunriseAdjustment = (
			0
			if hasSunRisen(
				self._chart.config,
				self.riseAndSet,
			)
			else -1
		)
		return weekdays[
			(
				self._chart._config[
					'date'
				].weekday()
				+ 1
				+ sunriseAdjustment
			)
			% daysInAWeek
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
