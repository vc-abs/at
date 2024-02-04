import pandas as pd
from core.helpers import (
	resolveRelativePath,
)

muhurtaYogaDF = pd.read_csv(
	resolveRelativePath(
		'./muhurtaYogaEffects.csv'
	)
)


def getMuhurtaYoga(panchang):
	vaara = panchang.vaara
	tithi = panchang.tithi
	nakshatra = panchang.nakshatra

	return muhurtaYogaDF.query(
		'tithi == @tithi and vaara == @vaara or '
		+ 'tithi == @tithi and nakshatra == @nakshatra or '
		+ 'vaara == @vaara and nakshatra == @nakshatra or '
		+ 'tithi == @tithi and vaara == @vaara and nakshatra == @nakshatra'
	)
