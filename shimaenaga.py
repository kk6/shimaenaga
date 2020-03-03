import os
import pathlib

from jinja2 import Environment, FileSystemLoader
import tomlkit

template_dir = pathlib.Path("./templates")
dest_dir = pathlib.Path("./dest")


def parse_config(config_file):
    with open(config_file) as f:
        config = tomlkit.parse(f.read())
    return config


def main():
    env = Environment(loader=FileSystemLoader(template_dir.resolve(), encoding="utf8"))
    template = env.get_template("index.j2")
    config = parse_config("config.toml")
    context = {"metadata": config["metadata"], "names": ["john", "alice"]}
    html = template.render(**context)
    if not dest_dir.exists():
        os.mkdir(dest_dir)
    with open(dest_dir / "index.html", mode="w") as f:
        f.write(str(html))


if __name__ == "__main__":
    main()
