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
        'blog_dir': 'Path of your blog',
        'blog_posts_dir': "blog's posts folder (relative to blog_dir)",
        'blog_images_dir': "blog's images folder (relative to blog_dir)",
        'templates_dir': "Path of folder of your custom templates (if any)",
        'working_dir': "Folder where keep your md, ipynb, html files",
        'google_analytics_id': 'It is in the snippet provided by google eg:UA-039224021-1',
        'disqus_username': 'It is in url of your disqus account eg: https://username.disqus.com/',
    }

    for k, v in sorted(blog_attrs.items()):
        try:
            hint = ' - {0}'.format(help[k])
            value = click.prompt(k + hint, default=v)

            if value.strip() == '':
                ctx.config.write('{0}:{1}'.format(blog, k), None)

            elif value != 'n':
                ctx.config.write('{0}:{1}'.format(blog, k), value)

        except KeyError:
        # The option is not supposed to be setup by user like defaultblog
            pass

