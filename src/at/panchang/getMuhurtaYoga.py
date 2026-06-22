import pandas as pd
from at.core.constants import (
	pakshaTithiCount,
)
from at.core.helpers import (
	resolveRelativePath,
)

muhurtaYogaDF = pd.read_csv(
	resolveRelativePath(
		'./muhurtaYogaEffects.csv'
	)
).assign(
	effect=lambda row: row['effect']
	* row['impact']
)


def getMuhurtaYogas(panchang):
	vaara = panchang.vaara
	pakshaTithi = (
		panchang.tithi % pakshaTithiCount
	)
	nakshatra = panchang.nakshatra
	queryLocals = {
		'vaara': vaara,
		'pakshaTithi': pakshaTithi,
		'nakshatra': nakshatra,
	}

	return muhurtaYogaDF.query(
		'(tithi == @pakshaTithi and vaara == @vaara and nakshatra.isna()) or '
		+ '(tithi == @pakshaTithi and vaara.isna() and nakshatra == @nakshatra) or '
		+ '(tithi.isna() and vaara == @vaara and nakshatra == @nakshatra) or '
		+ '(tithi == @pakshaTithi and vaara == @vaara and nakshatra == @nakshatra)',
		local_dict=queryLocals,
	)[['name', 'effect']]


def getMuhurtaYogaEffects(panchang):
	muhurtaYogas = getMuhurtaYogas(
		panchang
	)

	return {
		'positive': muhurtaYogas.query(
			'effect > 0'
		)['effect'].sum(),
		'negative': muhurtaYogas.query(
			'effect < 0'
		)['effect'].sum(),
		'yogas': ' '.join(
			muhurtaYogas['name']
		),
	}


__all__ = [
	getMuhurtaYogas,
	getMuhurtaYogaEffects,
]
