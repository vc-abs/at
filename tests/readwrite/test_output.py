from pathlib import Path

import pandas as pd

from at.readWrite.output import output


def test_output_exports_to_file_when_export_to_is_present(tmp_path: Path):
	out_file = tmp_path / 'out' / 'data.tsv'
	context = {
		'exportTo': str(out_file),
		'exportSeparator': '\t',
		'data': [
			{'scenario': 'e1', 'x': 1},
			{'scenario': 'e2', 'x': 2},
		],
	}

	output(context)

	assert out_file.exists()
	df = pd.read_csv(out_file, sep='\t')
	assert list(df.columns) == ['scenario', 'x']
	assert df.shape == (2, 2)


def test_output_prints_to_stdout_without_export_to(capsys):
	context = {
		'exportSeparator': '\t',
		'data': [{'scenario': 'e1', 'x': 1}],
	}

	output(context)
	captured = capsys.readouterr()
	assert 'scenario\tx' in captured.out
	assert 'e1\t1' in captured.out
