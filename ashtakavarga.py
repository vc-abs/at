import pandas as pd

from constants import ashtaka, houseCount
from chart import getObjects
from helpers import selectObjects

ashtakavargaBaseDF = pd.read_csv('./ashtakavarga.csv')
ashtakavargaBufferDF = ashtakavargaBaseDF.query('position == 1')\
	.drop(['position', 'points'], axis=1)

def getAshtakavarga(config):
	objects = getObjects(config)
	ashtakaObjects = selectObjects(objects, ashtaka)
	ashtakaObjectsDF = pd.DataFrame.from_records(ashtakaObjects, columns=['name', 'house', 'sign'])

	ashtakavargaDF = ashtakavargaBufferDF.merge(ashtakaObjectsDF, left_on='object', right_on='name')\
		.merge(ashtakaObjectsDF[['name', 'house']], left_on='reference', right_on='name')\
		.drop(columns=['name_x', 'name_y'])\
  	.rename(columns={'house_x': 'objectHouse', 'house_y': 'referenceHouse'})\
		.assign(position=lambda row: (row['objectHouse'] - row['referenceHouse']) % houseCount + 1)\
		.merge(ashtakavargaBaseDF, on=['object', 'reference', 'position'])\
		.query('reference == "mercury"')

	return ashtakavargaDF

__all__ = [getAshtakavarga]
