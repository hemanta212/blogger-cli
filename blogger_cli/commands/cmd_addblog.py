import click
from blogger_cli.cli import pass_context
from blogger_cli.commands.cmd_setupblog import setup


@click.command("addblog", short_help="Register a new blog")
@click.argument("blog")
@click.option("-v", "--verbose", is_flag=True)
@click.option("-s", "--silent", is_flag=True, help="Do not load the setup.")
@pass_context
def cli(ctx, blog, silent, verbose):
    """ Add a new blog.\n
    Usage:\n
    blogger addblog blogname\n
    blogger addblog -s blogname
    """

    ctx.verbose = verbose
    add_blog_if_valid(ctx, blog)

    if not silent:
        ctx.log("Running setup for", blog)
        setup(ctx, blog)


def add_blog_if_valid(ctx, blog, blog_dir=None):
    layout = {
        "blog_dir": blog_dir,
        "blog_posts_dir": None,
        "blog_images_dir": None,
        "templates_dir": None,
        "working_dir": None,
        "google_analytics_id": None,
        "disqus_username": None,
    }

    if not ctx.blog_exists(blog):
        ctx.config.write(blog, layout)
        ctx.log("Blog added succesfully")
        ctx.vlog("Blog", ctx.config.read(blog))
    else:
        ctx.log("Blog already exists!")
        ctx.vlog("Blogs", ctx.config.read(all_keys=True))
        raise SystemExit(0)
