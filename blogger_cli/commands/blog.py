import click
from blogger_cli.cli_utils import json_writer
from blogger_cli.cli import pass_context


@click.command('addblog', short_help="Register a new blog")
@click.option('-s', '--silent', is_flag=True,
              help="Do not load the setup.")
@click.option('-v', '--verbose', is_flag=True)
@pass_context
def cli(ctx, blog, silent, verbose):
    """ a repository."""
    if blog:
        ctx.blog = blog
    ctx.verbose = verbose
    print('good')
