import math
from at.core.cached import Cached
from at.core.constants import (
	sign_count,
	tithi_count,
	degrees,
	weekdays,
	days_in_a_week,
	weekday_lords,
	hora_lord_sequence,
	horas_per_day,
	nakshatras,
	nakshatra_count,
	padas_per_nakshatra,
)
from at.core.swe_helpers import (
	get_rise_and_set_times,
)
from at.core.helpers import (
	get_ordinal_position,
)
from at.panchang.get_muhurta_yoga import (
	get_muhurta_yogas,
	get_muhurta_yoga_effects,
)
from at.panchang.gowri import (
	get_gowri_schedule,
	get_current_gowri_segment,
	get_gowri_window_flags,
)


def get_object_distance(
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

	def _get_tithi(self):
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
				/ sign_count
			)
			% tithi_count
		)

	def _get_rise_and_set(self):
		return get_rise_and_set_times(
			self._chart._config
		)

	def _get_day_lengths(self):
		rise_and_set = self.rise_and_set
		event_time = self._chart.config[
			'datetime'
		]
		elapsed = int(
			(
				event_time
				- rise_and_set['sunrise']
			).total_seconds()
		)
		length = int(
			(
				rise_and_set['nextRise']
				- rise_and_set['sunrise']
			).total_seconds()
		)

		return {
			'elapsed': elapsed,
			'total': length,
		}

	def _get_tod(self):
		rise_and_set_times = self.rise_and_set

		return (
			'day'
			if (
				rise_and_set_times['sunrise']
				<= self._chart.config[
					'datetime'
				]
				< rise_and_set_times['sunset']
			)
			else 'night'
		)

	def _get_vaara(self):
		calendar_day_adjustment = (
			self.rise_and_set['sunrise'].day
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
				+ calendar_day_adjustment
			)
			% days_in_a_week
		]

	def _get_hora(self):
		vaara = self.vaara
		day_start_hora_lord_index = (
			hora_lord_sequence.index(
				weekday_lords[vaara]
			)
		)
		event_hora = int(
			horas_per_day
			* (
				self.day_lengths['elapsed']
				/ self.day_lengths['total']
			)
		)
		event_hora_lord_index = (
			day_start_hora_lord_index + event_hora
		) % days_in_a_week

		return hora_lord_sequence[
			event_hora_lord_index
		]

	def _get_nakshatra_number(self):
		return get_ordinal_position(
			self._chart.objects['moon'][
				'longitude'
			],
			nakshatra_count,
		)

	def _get_nakshatra(self):
		return nakshatras[
			self._get_nakshatra_number() - 1
		]

	def _get_nakshatra_pada(self):
		return (
			self._get_nakshatra_number() - 1
		) % padas_per_nakshatra + 1

	def _get_muhurta_yogas(self):
		return get_muhurta_yogas(self)

	def _get_muhurta_yoga_effects(self):
		return get_muhurta_yoga_effects(self)

	def _get_gowri_schedule(self):
		return get_gowri_schedule(self)

	def _get_gowri_segment(self):
		return get_current_gowri_segment(self)

	def _get_gowri(self):
		return get_gowri_window_flags(self)
