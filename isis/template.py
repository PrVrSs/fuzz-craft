from enum import Enum
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


TEMPLATES_PATH = Path(__file__).parent.resolve() / 'templates'


class TemplateEnum(Enum):
    PY_ATHERIS = 'py-atheris.jinja'
    C_CPP_LIBFUZZER = 'c-cpp-libfuzzer.jinja'


class Template:
    def __init__(self, template: TemplateEnum):
        self._env = Environment(
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=False,
            loader=FileSystemLoader(str(TEMPLATES_PATH)),
        )
        self._template = self._env.get_template(template.value)

    def render(self, **kwargs) -> str:
        return self._template.render(**kwargs)


def render(template: TemplateEnum, /, **kwargs: dict) -> str:
    return Template(template).render(**kwargs)
