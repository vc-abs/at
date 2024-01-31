from itertools import product
import pandas as pd

from constants import ashtaka, planets, signs, houseCount
from chart import getObjects
from helpers import selectObjects

ashtakavargaBaseDF = pd.read_csv('./ashtakavarga.csv')
ashtakavargaBufferDF = pd.DataFrame(
		product(signs, planets, ashtaka), columns=['sign', 'object', 'reference']
	)

def getAshtakavarga(config):
	objects = getObjects(config)
	ashtakaObjects = selectObjects(objects, ashtaka)
	ascSign = selectObjects(objects, ['asc'])[0]['sign']

	objectPositionsDF = pd.DataFrame.from_records(ashtakaObjects, columns=['name', 'sign'])\
		.rename(columns={ 'name': 'object'})

	ashtakavargaDF = ashtakavargaBufferDF.merge(
		objectPositionsDF, on='object', how='left'
	)\
	.rename(columns={ 'sign_x': 'sign', 'sign_y': 'objectSign'})\
	.merge(objectPositionsDF, left_on='reference', right_on='object', how='left')\
	.drop(columns=['object_y'])\
	.rename(columns={
		'object_x': 'object', 'sign_x': 'sign', 'sign_y': 'referenceSign'
  })\
	.assign(
		position=lambda row: (row['sign'] - row['referenceSign']) % houseCount + 1,
		house=lambda row: (houseCount + row['sign'] - ascSign) % houseCount + 1
	)\
	.merge(ashtakavargaBaseDF, on=['object', 'reference', 'position'])\
	.groupby('house')['points'].sum().to_dict()

	return ashtakavargaDF

__all__ = [getAshtakavarga]
