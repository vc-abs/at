from at.panchang.get_muhurta_yoga import (
	get_muhurta_yogas,
	get_muhurta_yoga_effects,
)


class _panchang:
	def __init__(self, tithi, vaara, nakshatra):
		self.tithi = tithi
		self.vaara = vaara
		self.nakshatra = nakshatra


def test_get_muhurta_yogas_returns_dataframe_with_expected_cols():
	p = _panchang(
		tithi=1,
		vaara='sunday',
		nakshatra='asvini',
	)
	df = get_muhurta_yogas(p)

	assert list(df.columns) == ['name', 'effect']
	assert len(df) >= 0


def test_get_muhurta_yoga_effects_shape():
	p = _panchang(
		tithi=1,
		vaara='sunday',
		nakshatra='asvini',
	)
	effects = get_muhurta_yoga_effects(p)

	assert set(effects.keys()) == {
		'positive',
		'negative',
		'yogas',
	}
	assert isinstance(effects['yogas'], str)


def test_get_muhurta_yoga_effects_counts_mild_positive_scores():
	p = _panchang(
		tithi=2,
		vaara='sunday',
		nakshatra='krittika',
	)
	effects = get_muhurta_yoga_effects(p)

	assert effects['positive'] == 3
	assert effects['negative'] == 0
	assert 'subhaMadhyam' in effects['yogas']
	assert 'tripushkara' in effects['yogas']


def test_get_muhurta_yoga_effects_uses_strict_negative_filter():
	p = _panchang(
		tithi=4,
		vaara='sunday',
		nakshatra='magha',
	)
	effects = get_muhurta_yoga_effects(p)

	assert effects['positive'] == 0
	assert effects['negative'] == -6
	assert 'visha' in effects['yogas']
	assert 'yamaghanta' in effects['yogas']
	assert 'nasa' in effects['yogas']
