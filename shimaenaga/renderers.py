import pathlib
from typing import Dict

from jinja2 import Environment, FileSystemLoader, Template


class Jinja2Renderer:

    themes_dir = pathlib.Path(__file__).parent / "themes"

    def __init__(self, theme: str, encoding: str = "utf8", ext: str = "j2"):
        self.env = Environment(
            loader=FileSystemLoader(
                str((self.themes_dir / theme / "templates").resolve()),
                encoding=encoding,
            ),
        )
        self.env.globals["ROOT"] = "/"
        self.ext = ext

    def _load_layout(self, name: str) -> Template:
        return self.env.get_template(f"{name}.{self.ext}")

    def render(self, layout_name: str, context: Dict) -> str:
        # FIXME: 引数 layout: Layout にして self._get_template(layout.name)
        #        -> template.render(dataclasses.asdict(layout)) でもいいかも
        layout = self._load_layout(layout_name)
        return layout.render(context)
