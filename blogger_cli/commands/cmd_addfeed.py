import os
from collections import OrderedDict

import click

from blogger_cli.blog_manager.add_post_meta import get_post_meta
from blogger_cli.cli import pass_context
from blogger_cli.commands.feed_utils.feed import (
    add_entry,
    setup_new_file,
    validate_entry,
)


@click.command("addfeed", short_help="Write to rss/atom feed")
@click.argument(
    "file_path", type=click.Path(exists=True, resolve_path=True), required=False
)
@click.option("-rss", "gen_rss", help="Generate rss file", is_flag=True)
@click.option("-i", "--interactive", is_flag=True, help="Edit feed entry editor")
@click.option("-t", "--title", "title", help="Title of post")
@click.option(
    "-c", "--content", "content", help="Content for mail or [File path] for content"
)
@click.option("-v", "--verbose", is_flag=True)
@click.option("--setup", is_flag=True, help="Setup feed for first time")
@click.option("-b", "--blog", help="Name of blog")
@pass_context
def cli(ctx, file_path, gen_rss, interactive, title, content, setup, blog, verbose):

    ctx.verbose = verbose
    blog = __get_blog(ctx, blog)
    ctx.current_blog = blog

    feed_type = "rss" if gen_rss else "atom"
    feed_file = ctx.config.read(blog + ":feed_file")

    if setup:
        run_setup(ctx, blog, feed_file, feed_type)

    elif not file_path:
        ctx.log(":: ERROR. <FILE> argument is not provided")
        raise SystemExit()

    elif not __is_valid_feed_file(ctx, blog):
        ctx.log(
            ":: ERROR parsing feed file! Review it or create new one using\n"
            "$ blogger addfeed -b <blogname> --setup"
        )
        raise SystemExit()

    ctx.log(":: PROCESSING ", file_path)
    feed_file = __get_feed_file(ctx, blog)

    if interactive:
        title, content = load_editor()

    post_meta = OrderedDict({"title": title, "content": content})
    post_meta = get_post_meta(ctx, file_path, post_meta)

    if not post_meta:
        return
    entry = validate_entry(ctx, post_meta)
    add_entry(ctx, feed_file, entry)
    ctx.log(":: Done")


def run_setup(ctx, blog, feed_file, feed_type):
    if not feed_file:
        feed_file = input("Path of feed file(relative to blog_dir) - ")
        ctx.config.write(blog + ":feed_file", feed_file)

    if __is_valid_feed_file(ctx, blog):
        if not click.confirm("Override existing feed file?"):
            raise SystemExit(0)

    feed_file = __get_feed_file(ctx, blog)
    # Create a new feed file
    setup_new_file(feed_file, feed_type)
    ctx.log("Setup successfully completed!")


def __get_blog(ctx, blog):
    if blog is None:
        default = ctx.default_blog
        if default is None:
            ctx.log("\nError: Missing option -b <blogname>")
            raise SystemExit()

        else:
            ctx.vlog("\nUsing default blog ->", default)
            blog = default
    return blog


def __get_feed_file(ctx, blog):
    feed_file = ctx.config.read(key=blog + ":feed_file")
    blog_dir = ctx.config.read(key=blog + ":blog_dir")

    if not feed_file:
        msg = (
            ":: ERROR. No feed_file found. Either make one using --setup flag\n"
            "or provide its path in config by:\n"
            "blogger config -b {blog} feed_file <path/of/feed/file>"
        )
        raise ctx.log(msg.format(blog=blog))
        raise SystemExit()

    feed_file_path = os.path.join(blog_dir, feed_file)
    return feed_file_path


def __is_valid_feed_file(ctx, blog):
    """
    Checks if a feed file path exists and it has any contents.
    If both are True then it returns True.

    If a feed_file is not found a new one is created.
    """

    feed_file = ctx.config.read(key=blog + ":feed_file")
    blog_dir = ctx.config.read(key=blog + ":blog_dir")
    if feed_file:
        # Create a new feed file and return false
        if not blog_dir:
            ctx.log(":: ERROR 'blog_dir' config is empty")
            raise SystemExit()
        feed_file_path = os.path.join(blog_dir, feed_file)
        if not os.path.exists(feed_file_path):
            ensure_feed_file(feed_file_path)
            return False

        # Read if the file has any contannts at all
        with open(feed_file_path, "r", encoding="utf-8") as rf:
            data = rf.read()
        if data:
            return True

    return False


def load_editor():
    marker = (
        "# Everything below this line is ignored\n"
        "Write title in first line, then content in next paragraph\n"
    )
    message = click.edit("\n\n" + marker)

    try:
        message = message.split(marker, 1)[0].rstrip("\n")
        if not message:
            raise ValueError
    except Exception:
        click.secho(":: ERROR empty file. Aborting...", bold=True, fg="bright_red")
        raise SystemExit()

    title_content = message.split("\n\n", maxsplit=1)
    title = title_content[0]
    content = ""
    if len(title_content) > 1:
        content = title_content[1]

    title, content = [i.strip() for i in (title, content)]
    return title, content


def ensure_feed_file(feed_file_path):
    try:
        with open(feed_file_path, "w"):
            return

    except FileNotFoundError:
        msg = (
            ":: ERROR Is the blog just created? \n",
            ":: Path: ",
            +feed_file_path + " doesnot exist",
            " \n:: TIP: Convert some files or export blog_layout",
            " or create folder manually",
        )
        click.secho(msg, bold=True, blink=True, fg="bright_red")
        raise SystemExit()
