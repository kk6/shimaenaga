import os

from .config import create_config_file, Config


def initialize(config: Config) -> None:
    create_config_file(config)
    create_directories()


def create_directories():
    for dirname in ("pages", "posts"):
        if not os.path.exists(dirname):
            os.mkdir(dirname)
