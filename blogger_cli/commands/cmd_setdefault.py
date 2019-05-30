import click
from blogger_cli.cli import pass_context


@click.command('defaultblog', short_help="Set a blog as default")
@click.argument('blog', type=str)
@click.option('-v', '--verbose', is_flag=True)
@pass_context
def cli(ctx, blog, verbose):
    """ Set a blog as default\n
    Usage:\n
    blogger defaultblog blogname
    """

    ctx.verbose = verbose
    if not ctx.blog_exists(blog):
        ctx.vlog('Blogs', ctx.blog_list)
        return ctx.log("No such blog ", blog)

    default_blog = ctx.default_blog
    if default_blog:
        ctx.vlog("Default blog", default_blog,
                 "found transferring its default property to", blog)
        ctx.config.delete_key(default_blog + ':default')
    ctx.config.write(blog + ':default', True)
    ctx.log('Default blog changed from', default_blog, "to", blog)
