import click

from fuzz_craft.codeql import LANGUAGE_QL_MAP, codeql
from fuzz_craft.file_manager import FileManager


@click.command(name='create_database')
@click.option('-l', '--language',
              type=click.Choice(tuple(LANGUAGE_QL_MAP.keys())))
@click.option('-ql', '--codeql_cmd',
              type=click.Path(dir_okay=False, resolve_path=True))
@click.option('-s', '--source',
              type=click.Path(file_okay=False, resolve_path=True))
def cli(language: str, codeql_cmd: str, source: str):
    codeql(
        language,
        codeql_cmd=codeql_cmd,
        file_manager=FileManager(source=source),
    ).init_database()
