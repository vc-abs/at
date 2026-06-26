from pathlib import Path
import sys

import pytest

SRC_ROOT = Path(__file__).resolve().parents[1] / 'src'

if str(SRC_ROOT) not in sys.path:
	sys.path.insert(0, str(SRC_ROOT))


@pytest.fixture
def repo_root():
	"""Absolute path to the repository root, independent of pytest's cwd."""
	return Path(__file__).resolve().parents[1]
