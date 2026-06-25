from at.chart import Chart
from at.readWrite.readConfig import readConfig


def test_chart_shadbala_balas_compute_for_real_preset_stack():
	config = readConfig(
		[
			'presets/archive/.vc.yml',
			'presets/debug.yml',
			'presets/allFieldSets.yml',
		]
	)
	scenario = config['scenarios']['VC']
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

	balas = chart.shadBala.balas

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


def test_chart_shadbala_balas_include_runtime_sensitive_components():
	config = readConfig(
		[
			'presets/archive/.vc.yml',
			'presets/debug.yml',
			'presets/allFieldSets.yml',
		]
	)
	scenario = config['scenarios']['VC']
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

	balas = chart.shadBala.balas
	mercury = balas['mercury']
	venus = balas['venus']

	assert isinstance(mercury['yuddhaBala'], (int, float))
	assert isinstance(venus['drikBala'], (int, float))
	assert isinstance(mercury['ayanaBala'], (int, float))
	assert isinstance(venus['abdaBala'], (int, float))
	assert isinstance(venus['maasaBala'], (int, float))
