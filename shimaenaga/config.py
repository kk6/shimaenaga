from dataclasses import dataclass, field
from datetime import date
from typing import Dict

import tomlkit

from .files import read_file


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
    metadata = tomlkit.table()
    metadata.add("title", config.sitemeta.title)
    metadata.add("author", config.sitemeta.author)
    metadata.add("language_code", config.sitemeta.language_code)
    metadata.add("year_of_publication", config.sitemeta.year_of_publication)
    doc.add("metadata", metadata)

    with open("config.toml", "w") as f:
        f.write(doc.as_string())


def parse_config(config_file: str) -> Dict:
    toml = read_file(config_file)
    return tomlkit.parse(toml)
