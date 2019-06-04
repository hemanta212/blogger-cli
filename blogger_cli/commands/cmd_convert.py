import os
import sys
import shutil
import click

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
@click.option('-noex', '--no-extract', 'extract_img', is_flag=True, default=True,
        help="Disable resource extraction from files like images from ipynbs")
@click.option('-v', '--verbose', is_flag=True,
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
    set_current_blog(ctx, blog)

    files_being_converted = get_files_being_converted(path)
    file_ext_map = get_file_ext_map(ctx, exclude_html, files_being_converted)
    destination_dir = check_and_ensure_destination_dir(ctx, destination_dir)
    img_dir = check_and_ensure_img_dir(ctx, destination_dir, img_dir)

    ctx.conversion = {
            'file_ext_map': file_ext_map,
            'destination_dir': destination_dir,
            'iscode': iscode,
            'img_dir': img_dir,
            'extract_img': extract_img
    }

    html_filenames = convert_and_copyfiles(ctx)
    for filename in html_filenames:
        add_post.add(ctx, filename)


def get_files_being_converted(path):
    isfolder = lambda x: True if os.path.isdir(x) else False
    all_files = []
    for item in path:
        if isfolder(item):
            item = get_all_files(item)
            all_files + item
        else:
            all_files.append(item)

    return all_files


def get_all_files(folder):
    files = []
    for file in os.listdir(folder):
        if os.path.isfile(file):
            files.append(file)
    return files


def check_and_ensure_destination_dir(ctx, output_dir):
    blog  = ctx.current_blog
    blog_dir = ctx.config.read(key=blog+': blog_dir')
    posts_dir = ctx.config.read(key=blog + ' : blog_posts_dir')

    if not posts_dir and not output_dir:
        ctx.log("No destination folder given. Specify one with -o option or",
            "setup in your", blog, "blog's config")
        ctx.exit("ERROR: NO OUTPUT FOLDER")

    if posts_dir:
        destination_dir = os.path.join(blog_dir, posts_dir)

    if output_dir:
        destination_dir = output_dir

    destination_dir = os.path.normpath(os.path.expanduser(destination_dir))
    return destination_dir


def check_and_ensure_img_dir(ctx, destination_dir, output_img_dir):
    blog = ctx.current_blog
    blog_dir = ctx.config.read(key=blog+': blog_dir')
    blog_img_dir = ctx.config.read(key=blog+': blog_images_dir')

    if not blog_img_dir and not output_img_dir:
        ctx.log("No destination folder given. Specify one with -o option or",
            "setup in your", blog, "blog's config")
        if click.confirm("Put images dir in same folder as blog posts?"):
            img_dir = os.path.join(destination_dir, 'images')
            return img_dir
        else:
            ctx.exit("ERROR: NO OUTPUT FOLDER")

    if blog_img_dir:
        img_dir = os.path.join(blog_dir, blog_img_dir)

    if output_img_dir:
        img_dir = output_img_dir

    img_dir = os.path.normpath(os.path.expanduser(img_dir))
    return img_dir


def set_current_blog(ctx, blog):
    current_blog = ctx.default_blog
    if blog:
        current_blog = blog

    if not ctx.blog_exists(current_blog):
        ctx.log("Blog name not given. Use --blog option or set default blog")
        ctx.exit("ERROR: Blogname unavailable. SEE blogger convert --help")

    ctx.current_blog = current_blog


def get_file_ext_map(ctx, exclude_html, files_being_converted):
    file_ext_map = {}

    if exclude_html:
        ctx.SUPPORTED_EXTENSIONS.remove('html')

    for file in files_being_converted:
        ext = get_file_ext(file)
        if ext in ctx.SUPPORTED_EXTENSIONS:
            file_ext_map[file] = ext
        else:
            ctx.log("Unsupported ext", ext, "Skipping")
            continue

    return file_ext_map


def get_file_ext(file):
    extension = os.path.splitext(file)[1]
    return extension[1:]

