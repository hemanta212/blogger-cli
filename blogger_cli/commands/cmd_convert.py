import os
import sys
import shutil
import click

from blogger_cli.commands.convert_utils.files import (gen_file_ext_map,
                                                convert_and_copyfiles)
from blogger_cli.blog_manager import add_post
from blogger_cli.cli import pass_context


@click.command('convert', short_help='Convert files to html')
@click.argument('path', nargs=-1, required=True,
                type=click.Path(exists=True))
@click.option('--not-code', 'iscode', is_flag=True, default=True,
        help="Do not add mathjax and code support")
@click.option('-o', 'destination_dir', type=click.Path(exists=True),
        help="Destination for converted files, DEFAULT  blog_config")
@click.option('-b', '--blog',
        help="Name of  the blag")
@click.option('-ex-html', '--exclude-html', 'exclude_html', is_flag=True,
        help='ignore html files from conversion')
@click.option('-v', '--verbose', is_flag=True,
        help="Enable verbose flag")
@pass_context
def cli(ctx, path, iscode, blog,
         destination_dir, exclude_html, verbose):
    """Convert from diffrent file format to html

   Usage:\n
    For files:\n
    blogger convert -f filename.ipynb\n
    blogger convert -f file1 file2 file3\n
    blogger convert -f filename --not-code

    For folder:\n
    blogger convert -F folder_with_files --type html\n
    blogger convert -F folder1 folder2 --type md --not-code
    """
    ctx.verbose = verbose
    set_current_blog(ctx, blog)
    set_files_being_converted(ctx, path)
    destination_dir = check_and_ensure_dest_dir(ctx, destination_dir)

    file_ext_map = gen_file_ext_map(ctx, exclude_html)
    html_filenames = convert_and_copyfiles(ctx, file_ext_map, destination_dir)
    for filename in html_filenames:
        add_post.add(ctx, filename, destination_dir, iscode)


def set_files_being_converted(ctx, path):
    isfolder = lambda x: True if os.path.isdir(x) else False
    all_files = []
    for item in path:
        if isfolder(item):
            item = get_all_files(item)
            all_files + item
        else:
            all_files.append(item)

    ctx.files_being_converted = all_files



def get_all_files(folder):
    files = []
    for file in os.listdir(folder):
        if os.path.isfile(file):
            files.append(file)
    return files


def check_and_ensure_dest_dir(ctx, output_dir):
    blog  = ctx.current_blog
    destination_dir = ctx.config.read(key=blog + ' : blog_posts_dir')
    if output_dir:
        destination_dir = output_dir

    if destination_dir is None:
        ctx.log("No destination folder given. Specify one with -o option or",
            "setup in your", blog, "blog's config")
        ctx.exit("ERROR: NO OUTPUT FOLDER")
    return destination_dir


def set_current_blog(ctx, blog):
    current_blog = ctx.default_blog
    if blog:
        current_blog = blog

    if not ctx.blog_exists(current_blog):
        ctx.log("Blog name not given. Use --blog option or set default blog")
        ctx.exit("ERROR: Blogname unavailable. SEE blogger convert --help")

    ctx.current_blog = current_blog
