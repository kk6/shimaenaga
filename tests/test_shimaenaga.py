import pytest
from unittest import mock
from textwrap import dedent


class TestParseConfig:
    @pytest.fixture
    def target(self):
        from shimaenaga import parse_config

        return parse_config

    @pytest.fixture
    def toml(self):
        s = """[metadata]
            title = "Site title"
            charset = "UTF-8"

            [directory]
            root = "."
            template = "templates"
            """
        return dedent(s)

    def test_it(self, target, toml):
        with mock.patch("shimaenaga.read_file", return_value=toml):
            result = target("path/to")
        assert result == {
            "metadata": {"title": "Site title", "charset": "UTF-8"},
            "directory": {"root": ".", "template": "templates"},
        }
