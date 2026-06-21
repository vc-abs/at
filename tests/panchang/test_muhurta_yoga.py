from at.panchang.getMuhurtaYoga import (
	getMuhurtaYogas,
	getMuhurtaYogaEffects,
)


class _Panchang:
	def __init__(self, tithi, vaara, nakshatra):
		self.tithi = tithi
		self.vaara = vaara
		self.nakshatra = nakshatra


def test_get_muhurta_yogas_returns_dataframe_with_expected_cols():
	p = _Panchang(
		tithi=1,
		vaara='sunday',
		nakshatra='asvini',
	)
	df = getMuhurtaYogas(p)

	assert list(df.columns) == ['name', 'effect']
	assert len(df) >= 0


def test_get_muhurta_yoga_effects_shape():
	p = _Panchang(
		tithi=1,
		vaara='sunday',
		nakshatra='asvini',
	)
	effects = getMuhurtaYogaEffects(p)

	assert set(effects.keys()) == {
		'positive',
		'negative',
		'yogas',
	}
	assert isinstance(effects['yogas'], str)
