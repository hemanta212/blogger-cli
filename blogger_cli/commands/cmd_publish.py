import click
from blogger_cli.cli import pass_context


@click.command('convert', short_help='Publish posts to blog')
@pass_context
def cli(ctx):
    """Publish posts to blog"""
    ctx.log("convert is not called")
