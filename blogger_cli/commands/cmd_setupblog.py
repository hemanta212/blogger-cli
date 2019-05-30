import click
from blogger_cli.cli import pass_context


@click.command('setupblog',  short_help="Register a new blog")
@click.argument('blog')
@click.option('-v', '--verbose', is_flag=True)
@pass_context
def cli(ctx, blog, verbose):
    """ Load a setup procedure to a blog.\n
    Usage:\n
        blogger setupblog blogname
    """
    ctx.verbose = verbose
    if not ctx.blog_exists(blog):
        ctx.log("Blog doesnot exist!")
    else:
        ctx.log("Setting up blog")
        setup(ctx, blog)
        ctx.log("Blog setup completed succesfully")


def setup(ctx, blog):
    ctx.log("Use n to skip through options!")
    blog_attrs = ctx.config.read(key=blog)
    help = {
        'blogname': 'Name of your blog',
        'blog_posts_dir':"Your blog's posts folder",
        'html_dir': 'Folder  you keep your unprocessed html file',
        'md_dir': 'Folder where you keep your md files',
        'ipynb_dir': 'Folder of your jupyter notebooks'
    }
    for k, v in sorted(blog_attrs.items()):
        hint = ' - {0}'.format(help[k])
        value = click.prompt(k + hint, default=v)
        if value != 'n':
            ctx.config.write('{0}:{1}'.format(blog, k), value)
