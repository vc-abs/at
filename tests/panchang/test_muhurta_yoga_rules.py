from at.panchang.getMuhurtaYoga import (
	getMuhurtaYogas,
)


class _Panchang:
	def __init__(self, tithi, vaara, nakshatra):
		self.tithi = tithi
		self.vaara = vaara
		self.nakshatra = nakshatra


def _get_yoga_names(
	tithi,
	vaara,
	nakshatra,
):
	return set(
		getMuhurtaYogas(
			_Panchang(
				tithi=tithi,
				vaara=vaara,
				nakshatra=nakshatra,
			)
		)['name'].tolist()
	)


def test_ravi_pushya_combo_matches():
	names = _get_yoga_names(
		tithi=1,
		vaara='sunday',
		nakshatra='pushya',
	)
	assert 'raviPushya' in names


def test_guru_pushya_combo_matches():
	names = _get_yoga_names(
		tithi=7,
		vaara='thursday',
		nakshatra='pushya',
	)
	assert 'guruPushya' in names


def test_tripushkara_combo_matches():
	names = _get_yoga_names(
		tithi=2,
		vaara='sunday',
		nakshatra='krittika',
	)
	assert 'tripushkara' in names


def test_negative_vaara_nakshatra_cluster_matches():
	names = _get_yoga_names(
		tithi=4,
		vaara='sunday',
		nakshatra='magha',
	)
	assert {
		'visha',
		'yamaghanta',
		'nasa',
	}.issubset(names)


def test_tithi_vaara_pair_rule_matches():
	names = _get_yoga_names(
		tithi=1,
		vaara='friday',
		nakshatra='asvini',
	)
	assert 'siddhaTithi' in names
