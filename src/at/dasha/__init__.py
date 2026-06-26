from datetime import timedelta
from at.core.cached import Cached
from at.core.constants import (
	days_per_year,
	nakshatra_width,
)

vimshottari_lengths = {
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
vimshottari_lengths_total = sum(
	vimshottari_lengths.values()
)
vimshottari_proportions = {
	planet: length
	/ vimshottari_lengths_total
	for planet, length in vimshottari_lengths.items()
}
vimshottari_sequence = list(
	vimshottari_lengths.keys()
)
dasha_count = len(vimshottari_sequence)
nakshatra_lord_count = len(
	vimshottari_sequence
)

double_cycle = (
	vimshottari_sequence
	+ vimshottari_sequence
)


def get_nakshatra_index(chart):
	return (
		chart.panchang.nakshatra_number - 1
	)


antar_dasha_prefixes = [
	'ad',
	'pad',
	'skd',
	'prd',
]
antar_dasha_max_depth = len(
	antar_dasha_prefixes
)


def get_antar_dasha(
	starting_planet,
	super_dasha_starts_at,
	super_dasha_length,
	covered_fraction,
	current_antar_dasha_depth=0,
	requested_antar_dasha_depth=None,
):
	if requested_antar_dasha_depth is None:
		requested_antar_dasha_depth = (
			current_antar_dasha_depth
		)

	covered_length = (
		covered_fraction * super_dasha_length
	)
	accumulated_length = 0
	current_antar_dasha_length = 0
	dasha_planet = None
	sequence_start = (
		vimshottari_sequence.index(
			starting_planet
		)
	)
	for current_planet in double_cycle[
		sequence_start:
	]:
		current_antar_dasha_length = (
			vimshottari_proportions[
				current_planet
			]
			* super_dasha_length
		)

		accumulated_length += (
			current_antar_dasha_length
		)
		dasha_planet = current_planet
		if (
			accumulated_length >= covered_length
		):
			break

	completed_length = (
		accumulated_length
		- current_antar_dasha_length
	)
	starts_at = (
		super_dasha_starts_at
		+ timedelta(
			days=completed_length * days_per_year
		)
	)
	ends_at = (
		super_dasha_starts_at
		+ timedelta(
			days=accumulated_length
			* days_per_year
		)
	)
	remaining_fraction = (
		accumulated_length - covered_length
	) / current_antar_dasha_length
	antar_dasha_prefix = antar_dasha_prefixes[
		requested_antar_dasha_depth
		- current_antar_dasha_depth
	]
	dasha_values = {
		antar_dasha_prefix: {
			'lord': dasha_planet,
			'startsAt': starts_at,
			'endsAt': ends_at,
			'remainder': remaining_fraction,
		}
	}

	sub_dasha_values = (
		get_antar_dasha(
			dasha_planet,
			starts_at,
			current_antar_dasha_length,
			1 - remaining_fraction,
			current_antar_dasha_depth - 1,
			requested_antar_dasha_depth,
		)
		if current_antar_dasha_depth
		else {}
	)

	return {
		**dasha_values,
		**sub_dasha_values,
	}


class Dasha(Cached):
	def __init__(self, chart):
		super().__init__()
		self._chart = chart

	def _get_nakshatra_lord(self):
		return {
			'nakshatraLord': vimshottari_sequence[
				get_nakshatra_index(self._chart)
				% nakshatra_lord_count
			],
		}

	def _get_dashas(self):
		maha_dasha = (
			self._get_maha_dasha()
		)
		start_date = maha_dasha['endsAt']
		dasha_start_index = (
			vimshottari_sequence.index(
				maha_dasha['lord']
			)
		)

		dashas = [maha_dasha]
		for i in range(1, dasha_count):
			planet_index = (
				dasha_start_index + i
			) % dasha_count
			planet = vimshottari_sequence[
				planet_index
			]
			dasha_period_years = (
				vimshottari_lengths[planet]
			)

			end_date = start_date + timedelta(
				days=dasha_period_years
				* days_per_year
			)
			dashas.append(
				{
					'lord': planet,
					'startsAt': start_date,
					'endsAt': end_date,
					'remainder': 1,
				}
			)

			start_date = end_date
		return dashas

	def _get_maha_dasha(self):
		event_time = self._chart.config[
			'datetime'
		]
		moon_position = self._chart.objects[
			'moon'
		]['longitude']
		nakshatra_index = get_nakshatra_index(
			self._chart
		)
		dasha_start_index = (
			nakshatra_index
			% nakshatra_lord_count
		)
		start_planet = vimshottari_sequence[
			dasha_start_index
		]
		nakshatra_start_degree = (
			nakshatra_index * nakshatra_width
		)
		covered_fraction = (
			moon_position
			- nakshatra_start_degree
		) / nakshatra_width
		remaining_dasha_period = (
			1 - covered_fraction
		)
		dasha_length = vimshottari_lengths[
			start_planet
		]
		covered_length = (
			dasha_length * covered_fraction
		)
		starts_at = event_time - timedelta(
			days=covered_length * days_per_year
		)
		ends_at = starts_at + timedelta(
			days=dasha_length * days_per_year
		)

		return {
			'lord': start_planet,
			'startsAt': starts_at,
			'endsAt': ends_at,
			'remainder': remaining_dasha_period,
		}

	def _get_antar_dashas(self):
		maha_dasha = self.maha_dasha
		covered_fraction = (
			1 - maha_dasha['remainder']
		)
		return get_antar_dasha(
			maha_dasha['lord'],
			maha_dasha['startsAt'],
			vimshottari_lengths[
				maha_dasha['lord']
			],
			covered_fraction,
			3,
		)
