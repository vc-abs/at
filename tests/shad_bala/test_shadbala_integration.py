from at.chart import Chart
from at.read_write.read_config import read_config


def test_chart_shadbala_balas_compute_for_real_preset_stack(repo_root):
	config = read_config(
		[
			str(repo_root / 'tests/fixtures/shadbala_scenario.yml'),
			str(repo_root / 'presets/debug.yml'),
			str(repo_root / 'presets/allFieldSets.yml'),
		]
	)
	scenario = config['scenarios']['referenceEvent']
	chart = Chart(
		{
			**config,
			'year': scenario['year'],
			'month': scenario['month'],
			'day': scenario['day'],
			'hour': scenario['hour'],
			'minute': scenario['minute'],
			'second': scenario['second'],
			'datetime': scenario['date'],
			'date': scenario['date'],
			'latitude': scenario['latitude'],
			'longitude': scenario['longitude'],
		}
	)

	balas = chart.shad_bala.balas

	assert set(balas.keys()) == {
		'sun',
		'moon',
		'mars',
		'mercury',
		'jupiter',
		'venus',
		'saturn',
	}
	assert all('shadBala' in bala for bala in balas.values())
	assert all('kaalaBala' in bala for bala in balas.values())
	assert all('digBala' in bala for bala in balas.values())
	assert all('drikBala' in bala for bala in balas.values())
	assert all('yuddhaBala' in bala for bala in balas.values())


def test_chart_shadbala_balas_include_runtime_sensitive_components(repo_root):
	config = read_config(
		[
			str(repo_root / 'tests/fixtures/shadbala_scenario.yml'),
			str(repo_root / 'presets/debug.yml'),
			str(repo_root / 'presets/allFieldSets.yml'),
		]
	)
	scenario = config['scenarios']['referenceEvent']
	chart = Chart(
		{
			**config,
			'year': scenario['year'],
			'month': scenario['month'],
			'day': scenario['day'],
			'hour': scenario['hour'],
			'minute': scenario['minute'],
			'second': scenario['second'],
			'datetime': scenario['date'],
			'date': scenario['date'],
			'latitude': scenario['latitude'],
			'longitude': scenario['longitude'],
		}
	)

	balas = chart.shad_bala.balas
	mercury = balas['mercury']
	venus = balas['venus']

	assert isinstance(mercury['yuddhaBala'], (int, float))
	assert isinstance(venus['drikBala'], (int, float))
	assert isinstance(mercury['ayanaBala'], (int, float))
	assert isinstance(venus['abdaBala'], (int, float))
	assert isinstance(venus['maasaBala'], (int, float))
