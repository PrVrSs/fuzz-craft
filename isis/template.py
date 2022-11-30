from pathlib import Path

from jinja2 import Environment, FileSystemLoader


TEMPLATES_PATH = Path(__file__).parent.resolve() / 'templates'


class Template:
    def __init__(self):
        self._env = Environment(
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=False,
            loader=FileSystemLoader(str(TEMPLATES_PATH)),
        )
        self._template = self._env.get_template('py-atheris.jinja')

    def render(self, function, arguments):
        return self._template.render(
            function=function,
            arguments=arguments,
        )
