from unittest.mock import patch

from at import main as main_mod


def test_main_uses_default_config_when_no_args():
	with patch.object(main_mod, 'read_config') as read_cfg, patch.object(
		main_mod, 'generate_combos'
	) as gen, patch.object(main_mod, 'output') as out:
		read_cfg.return_value = {'scenarios': {}, 'exportSeparator': '\t'}
		gen.return_value = []

		main_mod.main([])

		read_cfg.assert_called_once_with(
			main_mod.default_config_file_paths
		)
		gen.assert_called_once()
		out.assert_called_once()


def test_main_uses_passed_config_paths():
	with patch.object(main_mod, 'read_config') as read_cfg, patch.object(
		main_mod, 'generate_combos'
	) as gen, patch.object(main_mod, 'output') as out:
		read_cfg.return_value = {'scenarios': {}, 'exportSeparator': '\t'}
		gen.return_value = []

		main_mod.main(['a.yml', 'b.yml'])

		read_cfg.assert_called_once_with(['a.yml', 'b.yml'])
		gen.assert_called_once()
		out.assert_called_once()


def test_cli_uses_sys_argv_tail():
	with patch.object(main_mod, 'main') as main_fn, patch(
		'at.main.sys.argv', ['prog', 'x.yml']
	):
		main_mod.cli()
		main_fn.assert_called_once_with(['x.yml'])


def test_main_module_default_config_paths_are_defined():
	assert main_mod.default_config_file_paths == [
		'./examples/config.yml'
	]
