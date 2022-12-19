import click

from .commands import create_database, create_harness


@click.group()
def cli():
    pass


cli.add_command(create_database)
cli.add_command(create_harness)
