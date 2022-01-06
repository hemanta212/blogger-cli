import os
import click
from blogger_cli.cli import pass_context
from blogger_cli.commands.serve_utils import (
    get_free_port,
    is_port_occupied,
    serve_locally,
)


@click.command("serve", short_help="Serve your blog locally")
@click.argument("blog", required=False)
@click.option("--port", "-p", "port", type=int, default=get_free_port)
@click.option(
    "-d", "--dir", "given_dir", help="Folder path to serve. Default: blog_dir"
)
@click.option("-v", "--verbose", is_flag=True, help="Enable verbosity")
@pass_context
def cli(ctx, blog, port, given_dir, verbose):
    ctx.verbose = verbose
    ctx.vlog("\n:: GOT blog:", blog, "port:", str(port), "(", type(port), ")")

    blog = resolve_blog(ctx, blog)
    blog_dir = resolve_blog_dir(ctx, blog, given_dir)
    check_port_availability(ctx, port)

    ctx.vlog(":: Got blog_dir:", blog_dir)
    ctx.log(":: Serving at http://localhost:" + str(port) + "/")
    ctx.log(":: Exit using CTRL+C")

    serve_locally(blog_dir, port)


def resolve_blog(ctx, blog):
    if not blog:
        blog = ctx.default_blog
        ctx.vlog(":: No blog name given using default blog:", str(blog))
    if not blog:
        ctx.log("Use blogger serve <blogname> or set a default blog in configs")
        ctx.log("ERROR: Missing required argument 'BLOG' ")
        raise SystemExit()
    return blog


def resolve_blog_dir(ctx, blog, given_dir):
    blog_dir = ctx.config.read(key=blog + ":blog_dir")
    if given_dir:
        blog_dir = given_dir

    if not blog_dir:
        ctx.log("No blog_dir set blog_dir in config or use --dir option")
        ctx.log("ERROR: No folder specified")
        raise SystemExit()

    blog_dir = os.path.abspath(os.path.expanduser(blog_dir))
    return blog_dir


def check_port_availability(ctx, port):
    if is_port_occupied(port):
        ctx.log(
            " ERROR: The specified port is already in use.\n",
            "Please select other ports",
            "or let blogger get one automatically by omitting --port option",
        )
        raise SystemExit()
