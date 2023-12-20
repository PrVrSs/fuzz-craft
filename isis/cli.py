import click

from .commands import create_database, create_llm_harness


@click.group()
def cli():
    pass


cli.add_command(create_database)
cli.add_command(create_llm_harness)
