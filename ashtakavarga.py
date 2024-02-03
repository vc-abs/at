from itertools import product
import pandas as pd

from constants import (
	ashtaka,
	planets,
	signs,
	houseCount,
)
from helpers import select

ashtakavargaBaseDF = pd.read_csv(
	'./ashtakavarga.csv'
)
ashtakavargaBufferDF = pd.DataFrame(
	product(signs, planets, ashtaka),
	columns=[
		'sign',
		'object',
		'reference',
	],
)

columnRenameMap = {
	1: 'h1',
	2: 'h2',
	3: 'h3',
	4: 'h4',
	5: 'h5',
	6: 'h6',
	7: 'h7',
	8: 'h8',
	9: 'h9',
	10: 'h10',
	11: 'h11',
	12: 'h12',
}


def getAshtakavarga(objects):
	ashtakaObjects = list(
		select(objects, ashtaka).values()
	)
	ascSign = objects['asc']['sign']

	objectPositionsDF = (
		pd.DataFrame.from_records(
			ashtakaObjects,
			columns=['name', 'sign'],
		).rename(columns={'name': 'object'})
	)

	ashtakavargaDF = (
		ashtakavargaBufferDF.merge(
			objectPositionsDF,
			on='object',
			how='left',
		)
		.rename(
			columns={
				'sign_x': 'sign',
				'sign_y': 'objectSign',
			}
		)
		.merge(
			objectPositionsDF,
			left_on='reference',
			right_on='object',
			how='left',
		)
		.drop(columns=['object_y'])
		.rename(
			columns={
				'object_x': 'object',
				'sign_x': 'sign',
				'sign_y': 'referenceSign',
			}
		)
		.assign(
			position=lambda row: (
				row['sign']
				- row['referenceSign']
			)
			% houseCount
			+ 1,
			house=lambda row: (
				houseCount
				+ row['sign']
				- ascSign
			)
			% houseCount
			+ 1,
		)
		.merge(
			ashtakavargaBaseDF,
			on=[
				'object',
				'reference',
				'position',
			],
		)
		.groupby('house')['points']
		.sum()
		.rename(columnRenameMap)
	)

	return ashtakavargaDF


__all__ = [getAshtakavarga]
