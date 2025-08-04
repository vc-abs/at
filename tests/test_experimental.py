import math
import types

import pytest

import tools.experimental as exp


class DummyChart:
    def __init__(self, karakas=None, dasha=None, panchang=None, ashtakavarga=None):
        self.karakas = karakas or {}
        self.dasha = types.SimpleNamespace(startingDasha=dasha or {})
        self.panchang = types.SimpleNamespace(muhurtaYogaEffects=panchang or {})
        self.ashtakavarga = ashtakavarga or {}


def test_special_planet_pos_score_equal():
    chart = DummyChart(karakas={'amk': 'A'}, dasha={'lord': 'A'})
    result = exp._get_special_planet_pos_score(chart)
    assert result == {'specialPlanetPosScore': 1}


def test_special_planet_pos_score_not_equal():
    chart = DummyChart(karakas={'amk': 'X'}, dasha={'lord': 'Y'})
    result = exp._get_special_planet_pos_score(chart)
    assert result == {'specialPlanetPosScore': 0}


def test_bala_products(monkeypatch):
    # Stub external dependencies
    monkeypatch.setattr(
        'tools.generateCombos.getStartingAntarDashas',
        lambda chart: {'adRemainder': 2, 'adlStrength': 3, 'adlIshtaPhala': 4}
    )
    monkeypatch.setattr(
        'tools.generateCombos.getShadBalaStrength',
        lambda chart: {'totalS': 5, 'avgIP': 6}
    )
    chart = DummyChart()
    result = exp._get_bala_products(chart)
    # 2 * 3 * 4 * 5 * 6 = 720
    assert result['balaProduct'] == 720
    assert result['shortTermBalaProduct'] == 720


def test_muhurta_effect():
    chart = DummyChart(panchang={'positive': 7, 'negative': -2})
    result = exp._get_muhurta_effect(chart)
    assert result == {'muhurtaEffect': 5}


def test_ashtakavarga_sums():
    h = {f'h{i}': i for i in range(1, 13)}
    chart = DummyChart(ashtakavarga=h)
    result = exp._get_ashtakavarga_sums(chart)
    # apaduddharaka = 28*3 - (6+8+12) = 84 - 26 = 58
    assert result['apaduddharaka'] == exp._BINDU_PER_HOUSE * len(exp._APADUDDHARAKA_HOUSES) - sum(
        h[k] for k in exp._APADUDDHARAKA_HOUSES
    )
    assert result['gyana'] == h['h4'] + h['h5']
    assert result['samaj'] == sum(h[k] for k in exp._SAMAJ_HOUSES)


def test_artha_sutra_zero():
    # All zeros => p_one = -84, p_two = -112, p_three = -28, n_one = -84
    zeros = {f'h{i}': 0 for i in range(1, 13)}
    chart = DummyChart(ashtakavarga=zeros)
    result = exp._get_artha_sutra(chart)
    # compute expected
    p_one = -exp._BINDU_PER_HOUSE * len(exp._ARTHA_ONE_HOUSES)
    p_two = -exp._BINDU_PER_HOUSE * len(exp._ARTHA_TWO_HOUSES)
    p_three = 0 - exp._BINDU_PER_HOUSE
    n_one = -exp._BINDU_PER_HOUSE * len(exp._ARTHA_N_ONE_HOUSES)
    sign = lambda x: 1 if x > 0 else -1 if x < 0 else 0
    expected = (abs(p_one) ** 2.5 * sign(p_one)
                + abs(p_two) ** 2 * sign(p_two)
                + p_three
                - abs(n_one) ** 2 * sign(n_one))
    assert math.isclose(result['arthaSutra'], expected)


def test_health_metrics():
    h = {f'h{i}': 0 for i in range(1, 13)}
    # set plus and minus houses
    for k in exp._HEALTH_PLUS_HOUSES:
        h[k] = 2
    for k in exp._HEALTH_MINUS_HOUSES:
        h[k] = 1
    for k in exp._BVS_PLUS_HOUSES:
        h[k] = 3
    for k in exp._BVS_MINUS_HOUSES:
        h[k] = 1
    for k in exp._SATVIK_PLUS_HOUSES:
        h[k] = 5
    for k in exp._SATVIK_MINUS_HOUSES:
        h[k] = 2
    chart = DummyChart(ashtakavarga=h)
    result = exp._get_health_metrics(chart)
    health = sum(h[k] for k in exp._HEALTH_PLUS_HOUSES) - sum(h[k] for k in exp._HEALTH_MINUS_HOUSES)
    bvs = sum(h[k] for k in exp._BVS_PLUS_HOUSES) - sum(h[k] for k in exp._BVS_MINUS_HOUSES)
    satvik = sum(h[k] for k in exp._SATVIK_PLUS_HOUSES) - sum(h[k] for k in exp._SATVIK_MINUS_HOUSES)
    guided = health * abs(bvs) * satvik
    assert result == {'health': health, 'BvS': bvs, 'Satvik': satvik, 'GuidedS': guided}
