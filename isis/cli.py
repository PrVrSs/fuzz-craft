import click

from isis.codeql import create_database


@click.group()
def cli():
    pass


cli.add_command(create_database)
