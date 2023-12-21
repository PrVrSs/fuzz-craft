from operator import attrgetter

import click

from fuzz_craft.codeql import LANGUAGE_QL_MAP
from fuzz_craft.harness import Harness
from fuzz_craft.template import TemplateEnum


@click.command(name='create_harness')
@click.option('-l', '--language',
              type=click.Choice(tuple(LANGUAGE_QL_MAP.keys())))
@click.option('-ql', '--codeql_cmd',
              type=click.Path(dir_okay=False, resolve_path=True))
@click.option('-s', '--source',
              type=click.Path(file_okay=False, resolve_path=True))
@click.option('-t', '--template',
              type=click.Choice(tuple(map(attrgetter('value'), TemplateEnum))))
def cli(language, codeql_cmd, source, template):
    Harness(
        source=source,
        codeql_cmd=codeql_cmd,
        template=TemplateEnum(template),
        language=language,
    ).run()
