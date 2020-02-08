import json
from pathlib import Path
import click
from blogger_cli.cli import pass_context


@click.command("config", short_help="Change a blog's configurations")
@click.argument("configs", required=False, nargs=-1)
@click.option("-b", "--blog", type=str, help="Name of the blog to use")
@click.option("-rm", "--remove", is_flag=True, help="Enable delete key")
@click.option(
    "-re", "--restore", type=click.Path(exists=True), help="Restore a blog's config"
)
@click.option("-v", "--verbose", is_flag=True)
@pass_context
def cli(ctx, remove, blog, configs, restore, verbose):
    """
    Change a blogs configurations.\n
    Examples:\n
        blogger config -b <blogname> html_dir C:Users/foldername/\n
        blogger config -b <blogname> txt_dir ~/foldername/\n
    Tip: You can set a defalut blog to avoid using -b option everytime!
    """
    ctx.verbose = verbose
    blog = __get_blog(ctx, blog)
    if restore:
        with open(restore, "r") as rf:
            try:
                config_dict = json.load(rf)
            except Exception as E:
                ctx.log("ERROR: Invalid config file.", E)
                raise SystemExit(0)

        ctx.config.write(blog, config_dict)
        ctx.log("Configurations for", blog, "restored")
        raise SystemExit(0)

    if not configs:
        ctx.log("ERROR: MISSING ARGUMENT 'CONFIG KEY'", " \nSee blogger config --help")
        raise SystemExit()

    __validate(ctx, blog, configs)
    key = configs[0]
    blog_dict = ctx.config.read(key=blog)

    try:
        value = configs[1]
        if key in ["blog_dir", "templates_dir", "working_dir"]:
            value = ensure_and_expand_dir(value)

        ctx.config.write(blog + ":" + key, value)
        ctx.log(key, "->", value)
    except IndexError:
        if remove:
            ctx.config.delete_key(blog + ":" + key)
            ctx.log(key, "->", "deleted")
        else:
            ctx.log(blog_dict.get(key))
            raise SystemExit(0)


def ensure_and_expand_dir(dir):
    folder = Path(dir)
    try:
        full_path = str(folder.expanduser().resolve())
    except FileNotFoundError as E:
        msg = "ERROR:" + str(E) + str(dir)
        click.secho(msg, blink=True, bold=True, fg="bright_red")
        raise SystemExit()

    return full_path


def __get_blog(ctx, blog):
    if blog is None:
        default = ctx.default_blog
        if default is None:
            ctx.log("Try 'blogger config --help' for help.")
            raise SystemExit("\nError: Missing option -b <blogname>")

        else:
            ctx.vlog("\nUsing default blog ->", default)
            blog = default

    return blog


def __validate(ctx, blog, configs):
    if len(configs) > 2:
        raise SystemExit("\nInvalid input arguments")

    if not ctx.blog_exists(blog):
        raise SystemExit("\nBlog " + str(blog) + " doesnot exist")

    key = configs[0]
    blog_dict = ctx.config.read(key=blog)
    allowed_keys = ctx.config_keys + ctx.optional_config
    if key not in allowed_keys and key not in blog_dict:
        raise SystemExit("\nInvalid config key.")
