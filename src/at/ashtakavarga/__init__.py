from itertools import product
import pandas as pd
from at.core.helpers import (
	resolve_relative_path,
	select,
)
from at.core.constants import (
	ashtaka,
	planets,
	signs,
	house_count,
)

ashtakavarga_base_df = pd.read_csv(
	resolve_relative_path(
		'./ashtakavarga.csv'
	)
)
ashtakavarga_buffer_df = pd.DataFrame(
	product(signs, planets, ashtaka),
	columns=[
		'sign',
		'object',
		'reference',
	],
)

column_rename_map = {
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


def get_ashtakavarga(objects):
	ashtaka_objects = list(
		select(objects, ashtaka).values()
	)
	asc_sign = objects['asc']['sign']

	object_positions_df = (
		pd.DataFrame.from_records(
			ashtaka_objects,
			columns=['name', 'sign'],
		).rename(columns={'name': 'object'})
	)

	ashtakavarga_df = (
		ashtakavarga_buffer_df.merge(
			object_positions_df,
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
			object_positions_df,
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
			% house_count
			+ 1,
			house=lambda row: (
				house_count
				+ row['sign']
				- asc_sign
			)
			% house_count
			+ 1,
		)
		.merge(
			ashtakavarga_base_df,
			on=[
				'object',
				'reference',
				'position',
			],
		)
		.groupby('house')['points']
		.sum()
		.rename(column_rename_map)
	)

	return ashtakavarga_df


__all__ = [get_ashtakavarga]
