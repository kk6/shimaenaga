import pytest
import datetime
from textwrap import dedent

LOREM = dedent(
    """\
    Lorem ipsum dolor sit amet, consectetur adipiscing elit,
    sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
    nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit
    in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
    Excepteur sint occaecat cupidatat non proident,
    sunt in culpa qui officia deserunt mollit anim id est laborum.
    """
)


class TestContent:
    @pytest.fixture
    def target(self):
        from shimaenaga.contents import Content

        return Content

    def test_initialize(self, target):
        c = target(path="foo.md", title="Test title", body="Content body")
        assert c.path.name == "foo.md"
        assert c.title == "Test title"
        assert c.body == "Content body"

    def test_name(self, target):
        c = target("foo.md", "Test title", "Content body")
        assert c.name == "foo"

    def test_html(self, target):
        c = target("foo.md", "Test title", "Content body")
        assert c.html == "<p>Content body</p>\n"


class TestArticle:
    @pytest.fixture
    def target(self):
        from shimaenaga.contents import Article

        return Article

    def test_initialize(self, target):
        a = target(
            path="foo.md",
            title="Test title",
            date="2020-03-21",
            body="Content body",
            tags=["python", "blog"],
        )
        assert a.path.name == "foo.md"
        assert a.title == "Test title"
        assert a.body == "Content body"
        assert a.date == datetime.date(2020, 3, 21)
        assert a.tags == ["python", "blog"]

    def test_display_date(self, target):
        a = target(
            path="foo.md",
            title="Test title",
            date="2020-03-21",
            body="Content body",
            tags=["python", "blog"],
        )
        assert a.display_date == "Mar 21, 2020"

    def test_summarize_html(self, target):
        a = target(
            path="foo.md",
            title="Test title",
            date="2020-03-21",
            body=LOREM,
            tags=["python", "blog"],
        )
        assert a.summarize_html(length=30) == "<p>Lorem ipsum dolor sit...</p>"
