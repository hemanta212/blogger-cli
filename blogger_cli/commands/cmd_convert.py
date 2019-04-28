import click
from blogger_cli.cli import pass_context


@click.command('convert', short_help='Convert files to html')
@pass_context
def cli(ctx):
    """Convert diffrent file format to html"""
    ctx.log("convert is not called")
