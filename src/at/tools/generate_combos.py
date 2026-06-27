from collections.abc import Mapping
from functools import reduce
import pandas as pd
from at.chart import Chart
from at.read_write.get_default_config import (
	select_all_field_sets,
	select_all_query,
)
from at.core.constants import (
	planets,
	nodes,
	combustion_orbs,
)
from at.core.helpers import get_shortest_distance_in_circle
from at.core.planet_quality import get_planet_quality

order_map = {
	'ascending': True,
	'descending': False,
}


def get_object_houses(chart):
	return dict(
		{
			'asS': chart.objects['asc'][
				'sign'
			]
		},
		**{
			(object_key[:2] + 'H'): object[
				'house'
			]
			for (
				object_key,
				object,
			) in chart.objects.items()
			if object_key != 'asc'
		},
	)


def get_planetary_degrees(chart):
	return {
		'asD': chart.objects['asc'][
			'longitude'
		],
		**{
			f'{planet[:2]}D': chart.objects[planet][
				'longitude'
			]
			for planet in planets
		},
		**{
			f'{node[:2]}D': chart.objects[node][
				'longitude'
			]
			for node in nodes
		},
	}


place_holder_planet_balas = {
	'strength': 0,
	'ishtaPhala': 0,
}


def format_dasha_data(
	dasha, balas, prefix
):
	dasha_lord_phala = balas.get(
		dasha['lord'],
		place_holder_planet_balas,
	)

	return {
		**{
			f'{ prefix }{ k[0].upper() }{ k[1:] }': v
			for k, v in dasha.items()
		},
		f'{ prefix }lStrength': dasha_lord_phala[
			'strength'
		],
		f'{ prefix }lIshtaPhala': dasha_lord_phala[
			'ishtaPhala'
		],
	}


def get_maha_dasha(chart):
	return format_dasha_data(
		chart.dasha.maha_dasha,
		chart.shad_bala.balas,
		'md',
	)


def get_antar_dashas(chart):
	formatted_dashas = [
		format_dasha_data(
			antar_dasha_data,
			chart.shad_bala.balas,
			antar_dasha_prefix,
		)
		for antar_dasha_prefix, antar_dasha_data in chart.dasha.antar_dashas.items()
	]
	return {
		k: v
		for d in formatted_dashas
		for k, v in d.items()
	}


def get_planet_flags_by_planet(chart, planet):
	sun_longitude = chart.objects['sun']['longitude']
	planet_data = chart.objects[planet]
	flags = []

	if planet_data.get('retrograde'):
		flags.append('R')

	combustion_orb = combustion_orbs.get(planet)
	if combustion_orb and (
		get_shortest_distance_in_circle(
			planet_data['longitude'],
			sun_longitude,
		)
		<= combustion_orb
	):
		flags.append('C')

	return '|'.join(sorted(flags))


def get_planet_flags(chart):
	return {
		f'{planet[:2]}F': get_planet_flags_by_planet(
			chart, planet
		)
		for planet in planets
	}


def get_planet_qualities(chart):
	return {
		f'{planet[:2]}Q': get_planet_quality(
			chart.objects[planet], chart
		)
		for planet in planets
	}


time_flag_segments_by_vaara = {
	'sunday': {'RK': 8, 'YG': 5, 'GK': 7},
	'monday': {'RK': 2, 'YG': 4, 'GK': 6},
	'tuesday': {'RK': 7, 'YG': 3, 'GK': 5},
	'wednesday': {'RK': 5, 'YG': 2, 'GK': 4},
	'thursday': {'RK': 6, 'YG': 1, 'GK': 3},
	'friday': {'RK': 4, 'YG': 7, 'GK': 2},
	'saturday': {'RK': 3, 'YG': 6, 'GK': 1},
}


def is_within_day_segment(
	event_time,
	segment_index,
	day_start,
	day_end,
	segment_count=8,
):
	if not day_start <= event_time < day_end:
		return False

	segment_duration = (
		day_end - day_start
	) / segment_count
	segment_start = day_start + (
		segment_duration * (segment_index - 1)
	)
	segment_end = day_start + (
		segment_duration * segment_index
	)

	return segment_start <= event_time < segment_end



def get_time_flags(chart):
	rise_and_set = chart.panchang.rise_and_set
	event_time = chart.config['datetime']
	day_start = rise_and_set['sunrise']
	day_end = rise_and_set['sunset']
	flag_segments = time_flag_segments_by_vaara[
		chart.panchang.vaara
	]
	flags = [
		flag
		for flag, segment_index in flag_segments.items()
		if is_within_day_segment(
			event_time,
			segment_index,
			day_start,
			day_end,
		)
	]

	return {
		'timeF': '|'.join(sorted(flags))
	}



def get_gowri_flags(chart):
	gowri = chart.panchang.gowri
	return {
		'gowri': gowri['gowri'],
		'gowriScore': gowri['gowriScore'],
		'gowriM': gowri['gowriM'],
		'gowriS': gowri['gowriS'],
		'gowriT': gowri['gowriT'],
		'gowriStart': gowri['gowriStart'].strftime("%H:%M:%S"),
		'gowriEnd': gowri['gowriEnd'].strftime("%H:%M:%S"),
		'gowriF': gowri['gowriF'],
	}


phala_planet_count = 7


def get_shad_bala_strength(chart):
	strengths = {
		planet: phala['strength']
		for planet, phala in chart.shad_bala.balas.items()
	}

	avg_ishta_phala = (
		sum(
			phala['ishtaPhala']
			for phala in chart.shad_bala.balas.values()
		)
		/ phala_planet_count
	)

	return {
		**{
			f'{planet[:2]}S': strength
			for planet, strength in strengths.items()
		},
		'totalS': sum(strengths.values()),
		'avgIP': avg_ishta_phala,
	}


def get_karakas(chart):
	return chart.karakas

def get_panchang(chart):
	rise_and_set = chart.panchang.rise_and_set
	sunrise = rise_and_set['sunrise'].strftime("%H:%M:%S")
	sunset = rise_and_set['sunset'].strftime("%H:%M:%S")

	return {
		'tithi': chart.panchang.tithi,
		'nakshatra': chart.panchang.nakshatra,
		'vaara': chart.panchang.vaara,
		'sunrise': sunrise,
		'sunset': sunset,
  }

field_sets = {
	'muhurtaYogaEffects': {
		'fn': lambda chart: chart.panchang.muhurta_yoga_effects,
		'columns': ['positive', 'negative', 'yogas']
	},
	'objectHouses': {
		'fn': get_object_houses,
		'columns': ['asS','suH', 'moH', 'maH', 'meH', 'juH', 'veH', 'saH', 'raH', 'keH']
	},
	'planetaryDegrees': {
		'fn': get_planetary_degrees,
		'columns': ['asD', 'suD', 'moD', 'maD', 'meD', 'juD', 'veD', 'saD', 'raD', 'keD']
	},
	'ashtakavarga': {
		'fn': lambda chart: chart.ashtakavarga,
		'columns': ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12']
	},
	'mahaDasha': {
		'fn': get_maha_dasha,
		'columns': ['mdLord', 'mdStartsAt', 'mdEndsAt', 'mdRemainder', 'mdlStrength', 'mdlIshtaPhala']
	},
	'antarDashas': {
		'fn': get_antar_dashas,
		'columns': ['adLord', 'adStartsAt', 'adEndsAt', 'adRemainder', 'adlStrength', 'adlIshtaPhala', 'padLord', 'padStartsAt', 'padEndsAt', 'padRemainder', 'padlStrength', 'padlIshtaPhala', 'skdLord', 'skdStartsAt', 'skdEndsAt', 'skdRemainder', 'skdlStrength', 'skdlIshtaPhala','prdLord', 'prdStartsAt', 'prdEndsAt', 'prdRemainder', 'prdlStrength', 'prdlIshtaPhala']
	},
	'planetFlags': {
		'fn': get_planet_flags,
		'columns': ['suF', 'moF', 'maF', 'meF', 'juF', 'veF', 'saF']
	},
	'planetQualities': {
		'fn': get_planet_qualities,
		'columns': ['suQ', 'moQ', 'maQ', 'meQ', 'juQ', 'veQ', 'saQ']
	},
	'timeFlags': {
		'fn': get_time_flags,
		'columns': ['timeF']
	},
	'gowriFlags': {
		'fn': get_gowri_flags,
		'columns': ['gowri', 'gowriScore', 'gowriM', 'gowriS', 'gowriT', 'gowriStart', 'gowriEnd', 'gowriF']
	},
	'shadBalaStrength': {
		'fn': get_shad_bala_strength,
		'columns': ['suS', 'moS', 'maS', 'meS', 'juS', 'veS', 'saS', 'totalS', 'avgIP']
	},
	'karakas': {
		'fn': get_karakas,
		'columns': ['ak', 'amk', 'bk', 'mk', 'pk', 'gk', 'dk']
	},
	'scenario': {
		'fn': lambda chart: {},
		'columns': ['scenario', 'date', 'time']
	},
	'panchang': {
		'fn': get_panchang,
		'columns': ['tithi', 'nakshatra', 'vaara', 'sunrise', 'sunset']
	}
}

def get_fields(chart, sources=None):
	allowed_sources = set(sources) if sources is not None else None
	return reduce(
		lambda acc, field_set: {
			**acc,
			**field_sets[field_set[0]]['fn'](chart),
		} if allowed_sources is None or field_set[0] in allowed_sources else acc,
		field_sets.items(),
		{},
	)


def standardize_date(dt):
	return {
		'year': dt.year,
		'month': dt.month,
		'day': dt.day,
		'hour': dt.hour,
		'minute': dt.minute,
		'second': dt.second,
		'date': dt,
	}


def get_time_combos(
	scenario_name, config, dt
):
	chart = Chart(
		{
			**config,
			**standardize_date(dt),
			'datetime': dt,
		}
	)

	fields = get_fields(chart, config.get('sources'))

	return {
		'timestamp': dt,
		'scenario': scenario_name,
		**fields,
	}


def generate_scenario_combos(
	scenario_name, config
):
	scenario_config = config['scenarios'][scenario_name]
	config = {
		**config,
		**scenario_config,
	}
	time_series = (
		pd.date_range(
			start=config['date'],
			periods=config['count'],
			freq=config['interval'],
		)
		.to_pydatetime()
		.tolist()
	)

	return pd.DataFrame(
		list(
			map(
				lambda dt: get_time_combos(
					scenario_config.get('name', scenario_name), config, dt
				),
				time_series,
			)
		),
	)


class ConstantNamespace(Mapping):
	def __init__(self, data):
		self._data = data

	def __getattr__(self, key):
		try:
			value = self._data[key]
		except KeyError as exc:
			raise AttributeError(key) from exc
		return wrap_constants(value)

	def __getitem__(self, key):
		value = self._data[key]
		return wrap_constants(value)

	def __iter__(self):
		return iter(self._data)

	def __len__(self):
		return len(self._data)

	def __contains__(self, key):
		return key in self._data

	@property
	def ndim(self):
		return 0

	def __repr__(self):
		return repr(self._data)


def wrap_constants(value):
	if isinstance(value, ConstantNamespace):
		return value
	if isinstance(value, Mapping):
		return ConstantNamespace(value)
	return value


def get_computation_constants(config):
	computations = config.get('computations', {})
	if isinstance(computations, Mapping) and 'constants' in computations:
		return computations.get('constants', {})
	return config.get('constants', {})


def get_computation_fields(config):
	computations = config.get('computations', {})
	if isinstance(computations, Mapping) and 'fields' in computations:
		return computations.get('fields', {})
	return computations


def get_constant_namespace(config):
	return wrap_constants(get_computation_constants(config))


def rewrite_constants_expression(expression):
	parts = []
	i = 0
	in_single_quote = False
	in_double_quote = False

	while i < len(expression):
		char = expression[i]
		previous_char = expression[i - 1] if i > 0 else ''

		if char == "'" and not in_double_quote and previous_char != '\\':
			in_single_quote = not in_single_quote
			parts.append(char)
			i += 1
			continue

		if char == '"' and not in_single_quote and previous_char != '\\':
			in_double_quote = not in_double_quote
			parts.append(char)
			i += 1
			continue

		is_boundary = i == 0 or (
			previous_char not in '@._'
			and not previous_char.isalnum()
		)
		is_root_constants_reference = (
			not in_single_quote
			and not in_double_quote
			and expression.startswith('constants.', i)
			and is_boundary
		)
		if is_root_constants_reference:
			parts.append('@')

		parts.append(char)
		i += 1

	return ''.join(parts)


def get_expression_locals(config):
	return {
		'constants': get_constant_namespace(config),
	}


def resolve_constant_reference(value, config):
	if not (
		isinstance(value, str)
		and value.startswith('constants.')
	):
		return value

	resolved = get_computation_constants(config)
	for key in value.split('.')[1:]:
		resolved = resolved[key]
	return resolved


def process_summary_column(df, summary, config):
	summary_fn, summary_columns = next(
		iter(summary.items())
	)
	summary_columns = resolve_constant_reference(
		summary_columns, config
	)

	return getattr(
		df[summary_columns], summary_fn
	)(axis=1)


def get_column(df, column, config):
	if isinstance(column, str):
		rewritten_column = rewrite_constants_expression(
			column
		)
		return df.eval(
			rewritten_column,
			local_dict=get_expression_locals(config),
		)

	if isinstance(column, Mapping):
		return process_summary_column(
			df, column, config
		)

	return column


def add_custom_columns(df, columns, config):
	keys = list(columns.keys())

	for key in keys:
		df[key] = get_column(
			df, columns[key], config
		)


def sort_data(df, order):
	keys = list(order.keys())
	orders = list(
		map(
			lambda column: order_map[column],
			order.values(),
		)
	)

	return df.sort_values(
		by=keys,
		ascending=orders,
		kind='mergesort',
		inplace=True,
	)


def split_timestamp(df):
	df.insert(
		0,
		'date',
		df['timestamp'].map(
			lambda timestamp: timestamp.strftime(
				'%Y-%m-%d'
			)
		),
	)

	df.insert(
		1,
		'time',
		df['timestamp'].map(
			lambda timestamp: timestamp.strftime(
				'%H:%M:%S'
			)
		),
	)

	return df.drop(
		columns=['timestamp'], inplace=True
	)

def adjust_columns(df):
	scenario_column = df.pop('scenario')
	df.insert(0, 'scenario', scenario_column)

selection_types = {
	'all': lambda key, columns: field_sets[key]['columns'],
	'none': lambda key, columns: [],
	'some': lambda key, columns: columns,
}


_emitted_field_sets = {
	'computations': ['scenario', 'date', 'time'],
}


def _field_set_columns(field_set_name, selector):
	if selector == 'all':
		return field_sets[field_set_name]['columns']
	if selector == 'none':
		return []
	return selector


def add_columns(df, config_field_sets):
	columns_to_include = []
	for field_set_name, selector in config_field_sets.items():
		if field_set_name in _emitted_field_sets and selector == 'all':
			columns_to_include = columns_to_include + _emitted_field_sets[field_set_name]
			continue
		columns_to_include = columns_to_include + _field_set_columns(field_set_name, selector)
	return df[columns_to_include]


def generate_combos(config):
	df = pd.DataFrame()
	report = config['report']

	for scenario_name in config['scenarios'].keys():
		df = pd.concat(
			[
				df,
				generate_scenario_combos(
					scenario_name, config
				),
			],
		)

	add_custom_columns(
		df, get_computation_fields(config), config
	)
	split_timestamp(df)
	adjust_columns(df)
	filtered_df = df.query(
		rewrite_constants_expression(
			report.get('selection', select_all_query)
		),
		local_dict=get_expression_locals(config),
	)
	sort_data(filtered_df, report['order'])
	return add_columns(
		filtered_df, report.get('fieldSets', select_all_field_sets)
	)
