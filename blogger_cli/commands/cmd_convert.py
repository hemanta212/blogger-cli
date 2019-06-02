import os
import sys
import shutil
import click

from blogger_cli.commands.convert_utils.conversion import gen_conversion_class
from blogger_cli.commands.convert_utils.files import convert_and_copyfiles
from blogger_cli.blog_manager import add_post
from blogger_cli.cli import pass_context


@click.command('convert', short_help='Convert files to html')
@click.argument('path', nargs=-1, required=True,
                type=click.Path(exists=True))
@click.option('--not-code', 'iscode', is_flag=True, default=True,
        help="Do not add mathjax and code support")
@click.option('-o', 'destination_dir', type=click.Path(exists=True),
        help="Destination for converted files,DEFAULT from blog_config")
@click.option('-b', '--blog',
        help="Name of the blog")
@click.option('-ex-html', '--exclude-html', 'exclude_html', is_flag=True,
        help='Ignore html files from conversion')
@click.option('--img-dir', 'img_dir', type=click.Path(exists=True),
        help="Folder for post images. Default: blog's config, Destination dir")
@click.option('-noex', '--no-extract', 'extract_img', is_flag=True,
        help="Disable resource extraction from files like images from ipynbs")
@@click.option('-v', '--verbose', is_flag=True,
        help="Enable verbose flag")
@pass_context
def cli(ctx, path, iscode, blog, exclude_html, extract_img,
        destination_dir, img_dir, verbose):
    """
    Convert from diffrent file format to html

   Usage:\n
    For files:\n
    blogger convert filename.ipynb\n
    blogger convert file1 file2 file3 -b blog1 --exclude-html\n
    blogger convert filename --not-code -o ~/username.github.io

    blogger convert ../folder1 file1 ../folder2  -v
    """
    ctx.verbose = verbose
    Conversion = gen_conversion_class(ctx)
    conversion = Conversion(iscode, exclude_html, img_dir, extract_img)

    conversion.set_current_blog(blog)
    conversion.set_files_being_converted(path)
    conversion.set_file_ext_map()
    conversion.check_and_ensure_destination_dir(destination_dir)

    html_filenames = convert_and_copyfiles(conversion)
    for filename in html_filenames:
        add_post.add(filename, conversion)

