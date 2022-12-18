import click

from .commands import create_database


@click.group()
def cli():
    pass


cli.add_command(create_database)
