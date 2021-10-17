import pytest

from .config import Configuration
from .config_parser import parse_config

def test_parse_config():
    got = parse_config("config-devel.toml")
    assert got.database == "testdata/my_cash.gnucash"