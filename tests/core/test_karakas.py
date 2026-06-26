from at.core.karakas import get_karakas, sort_by_degree


class _chart:
	def __init__(self, objects):
		self.objects = objects


def test_sort_by_degree_prefers_higher_degree_within_sign():
	# 29 deg in sign should outrank 1 deg in sign
	a = {'longitude': 29.0}
	b = {'longitude': 1.0}
	assert sort_by_degree(a) < sort_by_degree(b)


def test_get_karakas_filters_to_day_rulers_and_orders_them():
	objects = {
		'sun': {'name': 'sun', 'longitude': 5.0},
		'moon': {'name': 'moon', 'longitude': 15.0},
		'mars': {'name': 'mars', 'longitude': 25.0},
		'mercury': {'name': 'mercury', 'longitude': 2.0},
		'jupiter': {'name': 'jupiter', 'longitude': 18.0},
		'venus': {'name': 'venus', 'longitude': 28.0},
		'saturn': {'name': 'saturn', 'longitude': 12.0},
		'rahu': {'name': 'rahu', 'longitude': 10.0},
		'ketu': {'name': 'ketu', 'longitude': 190.0},
	}
	chart = _chart(objects)
	karakas = get_karakas(chart)

	assert list(karakas.keys()) == [
		'ak',
		'amk',
		'bk',
		'mk',
		'pk',
		'gk',
		'dk',
	]
	# Highest in-sign degree among 7 day rulers is venus(28)
	assert karakas['ak'] == 'venus'
	# Ensure nodes are excluded
	assert 'rahu' not in karakas.values()
	assert 'ketu' not in karakas.values()
