import pandas as pd
from helpers import resolveRelativePath

tithiBaseDF = pd.read_csv(
	resolveRelativePath('./tithis.csv')
)


def getTithiDetails():
	return tithiBaseDF
