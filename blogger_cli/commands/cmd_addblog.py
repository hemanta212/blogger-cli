import click
from blogger_cli.cli import pass_context
from blogger_cli.commands.cmd_setupblog import setup


@click.command('addblog', short_help="Register a new blog")
@click.argument('blog')
@click.option('-v', '--verbose', is_flag=True)
@click.option('-s', '--silent', is_flag=True,
              help="Do not load the setup.")
@pass_context
def cli(ctx, blog, silent, verbose):
    """ Add a new blog.\n
    Usage:\n
    blogger addblog blogname\n
    blogger addblog -s blogname
    """

    ctx.verbose = verbose
    layout = {
        'blog_dir': None,
        'blog_posts_dir': None,
        'html_dir': None,
        'md_dir': None,
        'ipynb_dir': None,
    }

    if not ctx.blog_exists(blog):
        ctx.config.write(blog, layout)
        ctx.log("Blog added succesfully")
        ctx.vlog("Blog", ctx.config.read(blog))
    else:
        ctx.log("Blog already exists!")
        ctx.vlog('Blogs', ctx.config.read(all_keys=True))
        return None

    if not silent:
        ctx.log("Running setup for", blog)
        setup(ctx, blog)
        ctx.log("Setup completed succesfully")
