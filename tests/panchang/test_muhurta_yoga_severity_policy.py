import pandas as pd
import yaml


def test_yoga_policy_tracks_all_dataset_yogas(repo_root):
	csv_path = repo_root / 'src/at/panchang/muhurtaYogaEffects.csv'
	policy_path = repo_root / 'data/yogaWeightPolicy.yml'

	df = pd.read_csv(csv_path)
	with policy_path.open('r', encoding='utf-8') as f:
		policy = yaml.safe_load(f)

	yoga_names = set(df['name'].dropna().tolist())
	policy_names = set(
		policy['yogaPolicies'].keys()
	)

	assert yoga_names == policy_names


def test_yoga_policy_allowed_effects_match_dataset(repo_root):
	csv_path = repo_root / 'src/at/panchang/muhurtaYogaEffects.csv'
	policy_path = repo_root / 'data/yogaWeightPolicy.yml'

	df = pd.read_csv(csv_path)
	df['weightedEffect'] = (
		df['effect'] * df['impact']
	)

	with policy_path.open('r', encoding='utf-8') as f:
		policy = yaml.safe_load(f)

	for name, group in df.groupby('name'):
		actual = sorted(
			set(group['weightedEffect'].tolist())
		)
		expected = sorted(
			policy['yogaPolicies'][name][
				'allowedWeightedEffects'
			]
		)
		assert actual == expected
