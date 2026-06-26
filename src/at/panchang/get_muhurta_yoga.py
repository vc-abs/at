import pandas as pd
from at.core.constants import (
	paksha_tithi_count,
)
from at.core.helpers import (
	resolve_relative_path,
)

muhurta_yoga_df = pd.read_csv(
	resolve_relative_path(
		'./muhurtaYogaEffects.csv'
	)
).assign(
	effect=lambda row: row['effect']
	* row['impact']
)


def get_muhurta_yogas(panchang):
	vaara = panchang.vaara
	paksha_tithi = (
		panchang.tithi % paksha_tithi_count
	)
	nakshatra = panchang.nakshatra
	query_locals = {
		'vaara': vaara,
		'pakshaTithi': paksha_tithi,
		'nakshatra': nakshatra,
	}

	return muhurta_yoga_df.query(
		'(tithi == @pakshaTithi and vaara == @vaara and nakshatra.isna()) or '
		+ '(tithi == @pakshaTithi and vaara.isna() and nakshatra == @nakshatra) or '
		+ '(tithi.isna() and vaara == @vaara and nakshatra == @nakshatra) or '
		+ '(tithi == @pakshaTithi and vaara == @vaara and nakshatra == @nakshatra)',
		local_dict=query_locals,
	)[['name', 'effect']]


def get_muhurta_yoga_effects(panchang):
	muhurta_yogas = get_muhurta_yogas(
		panchang
	)

	return {
		'positive': muhurta_yogas.query(
			'effect > 0'
		)['effect'].sum(),
		'negative': muhurta_yogas.query(
			'effect < 0'
		)['effect'].sum(),
		'yogas': ' '.join(
			muhurta_yogas['name']
		),
	}


__all__ = [
	get_muhurta_yogas,
	get_muhurta_yoga_effects,
]
