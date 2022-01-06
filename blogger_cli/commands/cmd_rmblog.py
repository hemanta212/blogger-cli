import click
from blogger_cli.cli import pass_context


@click.command("rmblog", short_help="Remove a blog")
@click.argument("blog")
@click.option("-v", "--verbose", is_flag=True)
@pass_context
def cli(ctx, blog, verbose):
    """ Remove a blog"""
    ctx.verbose = verbose
    if not ctx.blog_exists(blog):
        ctx.log("Blog doesnot exist! so not removed")
        ctx.vlog("Blogs: ", ctx.blog_list)
    else:
        ctx.config.delete_key(blog)
        ctx.log("Blog removed succesfully")
