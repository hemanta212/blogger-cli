import click
from blogger_cli.cli import pass_context


@click.command('config', short_help="Change a blog's configurations")
@click.argument('configs', required=True, nargs=-1)
@click.option('-b', '--blog', type=str, help="Name of the blog to use")
@click.option('-rm', '--remove', is_flag=True, help="Enable delete key")
@click.option('-v', '--verbose', is_flag=True)
@pass_context
def cli(ctx, remove, blog, configs, verbose):
    """
    Change a blogs configurations.\n
    Examples:\n
        blogger config -b <blogname> html_dir C:Users/foldername/\n
        blogger config -b <blogname> txt_dir ~/foldername/\n
    Tip: You can set a defalut blog to avoid using -b option everytime!
    """
    ctx.verbose = verbose
    blog = __get_blog(ctx, blog)
    __validate(ctx, blog, configs)
    key = configs[0]
    blog_dict = ctx.config.read(key=blog)

    try:
        value = configs[1]
        ctx.config.write(blog + ":" + key, value)
        ctx.log(key, "->", value)
    except IndexError:
        if remove:
            ctx.config.delete_key(blog + ':' + key)
            ctx.log(key, "->", "deleted")
        else:
            ctx.log(blog_dict.get(key))


def __get_blog(ctx, blog):
    if blog is None:
        default = ctx.default_blog
        if default is None:
            ctx.exit("Try 'blogger config --help' for help.",
                     "\nError: Missing option -b <blogname>")
        else:
            ctx.vlog("\nUsing default blog ->", default)
            blog = default

    return blog


def __validate(ctx, blog, configs):
    if len(configs) > 2:
        ctx.exit("\nInvalid input arguments")

    if not ctx.blog_exists(blog):
        ctx.exit("\nBlog", blog, "doesnot exist")

    key = configs[0]
    blog_dict = ctx.config.read(key=blog)
    if key not in ctx.config_keys and key not in blog_dict:
        ctx.exit("\nInvalid config key.")
