from ..codeql import codeql, LANGUAGE_QL_MAP

import click


@click.command(name='create_database')
@click.option('-l', '--language',
              type=click.Choice(tuple(LANGUAGE_QL_MAP.keys())))
@click.option('-ql', '--codeql_cmd',
              type=click.Path(dir_okay=False, resolve_path=True))
@click.option('-s', '--source',
              type=click.Path(file_okay=False, resolve_path=True))
def cli(language, codeql_cmd, source):
    codeql(
        language,
        codeql_cmd=codeql_cmd,
        source=source,
    ).init_database()
