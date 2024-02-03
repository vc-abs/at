from itertools import product
import pandas as pd
from helpers import resolveRelativePath
from constants import tithis, weekDays

tithiBaseDF = (
	pd.DataFrame(
		product(tithis, weekDays),
		columns=['tithi', 'vaar'],
	)
	.assign(effect=0)
	.merge(
		pd.read_csv(
			resolveRelativePath(
				'./tithis.csv'
			)
		),
	)
).merge(
	pd.read_csv(
		resolveRelativePath(
			'./tithiVaarEffects.csv'
		)
	),
	on=['tithi', 'vaar'],
	how='left',
)

print(
	tithiBaseDF.query(
		'vaar == "wednesday"'
	)
)

defaultProps = {'effect': 'neutral'}


def getTithiDetails(chart):
	result = tithiBaseDF.query(
		'tithi == @chart.tithi and vaar == @chart.vaar'
	)
	props = (
		result.iloc[0].to_dict()
		if len(result)
		else defaultProps
	)

	return {
		'tithi': chart.tithi,
		'vaar': chart.vaar,
		**props,
	}
