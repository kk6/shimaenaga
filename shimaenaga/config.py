from dataclasses import field
from datetime import date

from pydantic.dataclasses import dataclass
import tomlkit

from .files import read_file, write_file


@dataclass
class SiteMeta:
    title: str = "Site title"
    author: str = "yourname"
    language_code: str = "en"
    year_of_publication: int = field(default_factory=lambda: date.today().year)


@dataclass
class Config:
    theme: str = "simple"
    sitemeta: SiteMeta = SiteMeta()


default_config = Config()


def create_config_file(config: Config) -> None:
    doc = tomlkit.document()
    doc.add("theme", config.theme)
    sitemeta = tomlkit.table()
    sitemeta.add("title", config.sitemeta.title)
    sitemeta.add("author", config.sitemeta.author)
    sitemeta.add("language_code", config.sitemeta.language_code)
    sitemeta.add("year_of_publication", config.sitemeta.year_of_publication)
    doc.add("sitemeta", sitemeta)
    write_file("config.toml", doc.as_string())


def parse_config(config_file: str) -> Config:
    toml = read_file(config_file)
    c = tomlkit.parse(toml)
    sitemeta = c["sitemeta"]
    config = Config(
        theme=c["theme"],
        sitemeta=SiteMeta(
            title=sitemeta["title"],
            author=sitemeta["author"],
            language_code=sitemeta["language_code"],
        ),
    )
    return config
