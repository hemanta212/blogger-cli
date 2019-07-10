import os
import click
from blogger_cli.cli import pass_context
from blogger_cli.commands.export_utils.copier import (copy_design_assets,
                    copy_blog_index, copy_blog_config, copy_blog_template,
                    copy_blog_layout)

@click.command('export', short_help="Export default design to your blog")
@click.argument('resource', type=str)
@click.option('-b', '--blog', type=str, help="Name of the blog to use")
@click.option('-o', '--to', 'relative_path',
        help="Relative path from blog root")
@click.option('-v', '--verbose', is_flag=True,
        help='Enable verbose flag')
@pass_context
def cli(ctx,  resource, blog, relative_path, verbose):
    """
    Export necessary resources to bootstrap your blog\n
    Syntax: \n
        blogger export [OPTION} [RESOURCE} [RELATIVE BLOG PATH}\n
    Examples:\n
        blogger export -b <blogname> <resource> blogs/\n
    Tip: You can set a defalut blog to avoid using -b option everytime!\n
        blogger export <resource> assets/css/\n

   RESOURCES:\n
        design_assets,
        blog_template,
        blog_index,
        blog_config
        blog_layout
    """
    ctx.verbose = verbose
    validate_blog_and_settings(ctx, blog, relative_path)
    export_path = resolve_export_path(ctx, relative_path)

    resource_map = {
        'design_assets': copy_design_assets,
        'blog_template': copy_blog_template,
        'blog_index': copy_blog_index,
        'blog_config': copy_blog_config,
        'blog_layout':copy_blog_layout,
    }

    transfer = resource_map.get(resource)
    if not transfer:
        ctx.log("No such resource. See blogger export --help")
        raise SystemExit("ERROR: INVALID RESOURCE NAME")

    ctx.vlog("Using function", transfer)
    transfer(ctx, export_path)


def validate_blog_and_settings(ctx, input_blog, input_path):
    blog = ctx.default_blog
    if input_blog:
        blog = input_blog

    blog_exists = ctx.blog_exists(blog)
    if blog_exists:
            settings = ctx.config.read(key=blog + ': blog_dir')
            if not settings and not input_path:
                ctx.log("Set config value for blog_dir in", blog, "blog")
                raise SystemExit("ERROR: MISSING CONFIG: blog_dir")

    elif not blog or not blog_exists:
        ctx.log("Pass a correct blog  with -b option",
                "or set a default blog")
        raise SystemExit("ERROR: INVALID_BLOG_NAME: " + str(blog))

    ctx.current_blog = blog


def resolve_export_path(ctx, relative_path):
    blog = ctx.current_blog
    blog_dir = ctx.config.read(key=blog+': blog_dir')
    if not blog_dir:
        if not os.path.exists(os.path.dirname(relative_path)):
            ctx.log("You have used relative path", relative_path,
                    'without setting blog_dir value in config!')
            raise SystemExit("Use full path to export in this folder")
        else:
            blog_dir = ''

    blog_dir = os.path.normpath(os.path.expanduser((blog_dir)))

    export_path = blog_dir
    if relative_path:
        export_path = os.path.join(blog_dir, relative_path)

    try:
        os.makedirs(export_path)
    except FileExistsError:
        pass

    ctx.vlog("Got export path", export_path)
    return export_path
