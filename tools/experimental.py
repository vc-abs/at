import math

# Constants for Ashtakavarga and Bala calculations
_BINDU_PER_HOUSE = 28
_DEFAULT_STRENGTH_FALLBACK = 1
_DEFAULT_ISHTA_PHALA_FALLBACK = 30

# House groupings for various metrics
_APADUDDHARAKA_HOUSES = ('h6', 'h8', 'h12')
_GYANA_HOUSES = ('h4', 'h5')
_SAMAJ_HOUSES = ('h1', 'h2', 'h3', 'h7', 'h10')
_ARTHA_ONE_HOUSES = ('h1', 'h7', 'h11')
_ARTHA_TWO_HOUSES = ('h3', 'h5', 'h9', 'h10')
_ARTHA_THREE_HOUSES = ('h4',)
_ARTHA_N_ONE_HOUSES = ('h6', 'h8', 'h12')
_HEALTH_PLUS_HOUSES = ('h3', 'h7', 'h11')
_HEALTH_MINUS_HOUSES = ('h4', 'h8', 'h12')
_BVS_PLUS_HOUSES = ('h1', 'h5', 'h9')
_BVS_MINUS_HOUSES = ('h2', 'h6', 'h10')
_SATVIK_PLUS_HOUSES = ('h1', 'h4', 'h7', 'h10', 'h5', 'h9')
_SATVIK_MINUS_HOUSES = ('h2', 'h3', 'h6', 'h8', 'h7', 'h12')

def _get_special_planet_pos_score(chart):
	amk = chart.karakas['amk']
	d_lord = chart.dasha.startingDasha['lord']
	return {
		'specialPlanetPosScore': 1 if amk == d_lord else 0
	}

def _get_bala_products(chart):
	from tools.generateCombos import getStartingAntarDashas, getShadBalaStrength
	antar = getStartingAntarDashas(chart)
	d_remainder = antar.get('adRemainder', 0)
	d_l_strength = antar.get('adlStrength', 0)
	d_l_ishta_phala = antar.get('adlIshtaPhala', 0)
	shad = getShadBalaStrength(chart)
	total_s = shad.get('totalS', 0)
	avg_ip = shad.get('avgIP', 0)

	bala_product = (
		d_remainder
		* (d_l_strength if d_l_strength > 0 else _DEFAULT_STRENGTH_FALLBACK)
		* (d_l_ishta_phala if d_l_ishta_phala > 0 else _DEFAULT_ISHTA_PHALA_FALLBACK)
		* total_s
		* avg_ip
	)
	short_term_bala_product = (
		math.ceil(d_remainder)
		* (d_l_strength if d_l_strength > 0 else _DEFAULT_STRENGTH_FALLBACK)
		* (d_l_ishta_phala if d_l_ishta_phala > 0 else _DEFAULT_ISHTA_PHALA_FALLBACK)
		* total_s
		* avg_ip
	)
	return {
		'balaProduct': bala_product,
		'shortTermBalaProduct': short_term_bala_product,
	}

def _get_muhurta_effect(chart):
	mu_effect = chart.panchang.muhurtaYogaEffects
	return {
		'muhurtaEffect': (
			mu_effect.get('positive', 0)
			+ mu_effect.get('negative', 0)
		)
	}

def _get_ashtakavarga_sums(chart):
	h = chart.ashtakavarga
	apaduddharaka = (
		_BINDU_PER_HOUSE * len(_APADUDDHARAKA_HOUSES)
		- sum(h.get(k, 0) for k in _APADUDDHARAKA_HOUSES)
	)
	gyana = sum(h.get(k, 0) for k in _GYANA_HOUSES)
	samaj = sum(h.get(k, 0) for k in _SAMAJ_HOUSES)
	return {
		'apaduddharaka': apaduddharaka,
		'gyana': gyana,
		'samaj': samaj,
	}

def _get_artha_sutra(chart):
	h = chart.ashtakavarga

	def sign(x):
		return 1 if x > 0 else -1 if x < 0 else 0

	p_one = (
		sum(h.get(k, 0) for k in _ARTHA_ONE_HOUSES)
		- (_BINDU_PER_HOUSE * len(_ARTHA_ONE_HOUSES))
	)
	p_two = (
		sum(h.get(k, 0) for k in _ARTHA_TWO_HOUSES)
		- (_BINDU_PER_HOUSE * len(_ARTHA_TWO_HOUSES))
	)
	p_three = sum(h.get(k, 0) for k in _ARTHA_THREE_HOUSES) - _BINDU_PER_HOUSE
	n_one = (
		sum(h.get(k, 0) for k in _ARTHA_N_ONE_HOUSES)
		- (_BINDU_PER_HOUSE * len(_ARTHA_N_ONE_HOUSES))
	)

	artha_sutra = (
		abs(p_one) ** 2.5 * sign(p_one)
		+ abs(p_two) ** 2 * sign(p_two)
		+ p_three
		- abs(n_one) ** 2 * sign(n_one)
	)
	return {'arthaSutra': artha_sutra}

def _get_health_metrics(chart):
	h = chart.ashtakavarga
	health = (
		sum(h.get(k, 0) for k in _HEALTH_PLUS_HOUSES)
		- sum(h.get(k, 0) for k in _HEALTH_MINUS_HOUSES)
	)
	bvs = (
		sum(h.get(k, 0) for k in _BVS_PLUS_HOUSES)
		- sum(h.get(k, 0) for k in _BVS_MINUS_HOUSES)
	)
	satvik = (
		sum(h.get(k, 0) for k in _SATVIK_PLUS_HOUSES)
		- sum(h.get(k, 0) for k in _SATVIK_MINUS_HOUSES)
	)
	guided_s = health * abs(bvs) * satvik
	return {
		'health': health,
		'BvS': bvs,
		'Satvik': satvik,
		'GuidedS': guided_s,
	}

def getExperimental(chart):
	return {
		**_get_special_planet_pos_score(chart),
		**_get_bala_products(chart),
		**_get_muhurta_effect(chart),
		**_get_ashtakavarga_sums(chart),
		**_get_artha_sutra(chart),
		**_get_health_metrics(chart),
	}
