import pytest
from unittest import mock
from textwrap import dedent
from dataclasses import asdict


class TestParseConfig:
    @pytest.fixture
    def target(self):
        from shimaenaga.config import parse_config

        return parse_config

    @pytest.fixture
    def toml(self):
        s = dedent(
            """\
            theme = "simple"
            [sitemeta]
            title = "Site title"
            author = "your name"
            language_code = "en"
            year_of_publication = 2020
            """
        )
        return dedent(s)

    def test_it(self, target, toml):
        with mock.patch("shimaenaga.config.read_file", return_value=toml):
            result = target("path/to")
        assert asdict(result) == {
            "theme": "simple",
            "sitemeta": {
                "title": "Site title",
                "author": "your name",
                "language_code": "en",
                "year_of_publication": 2020,
            },
        }
