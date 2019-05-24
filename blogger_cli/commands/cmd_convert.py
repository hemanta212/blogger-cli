import os
import sys
import shutil
import click

from blogger_cli.converter import ipynb_to_html, md_to_html
from blogger_cli.blog_manager import add_post
from blogger_cli.cli import pass_context

BLOG_POSTS_DIR = os.path.expanduser('~/hemanta212.github.io/blog')

@click.command('convert', short_help='Convert files to html')
@click.argument('path', type=click.Path())
@click.option('-f', '--file', is_flag=True)
@click.option('-F', '--folder', is_flag=True)
@click.option('--iscode', is_flag=True, default=True)
@click.option('-t', '--type')
@click.option('-v', '--verbose', is_flag=True)

@pass_context
def cli(ctx, path, iscode, type, file, folder, verbose):
    """Convert diffrent file format to html"""
    ctx.verbose = verbose
    if not type:
        type = get_file_type(path)
    if file:
        ctx.vlog("Processing the file", path)
        process_file(path, iscode, type)
    elif folder:
        ctx.vlog("Processing the folder", path)
        process_folder(path, type)
    else:
        ctx.log("ERROR: Please specify file or folder with -f or -F")

def get_file_type(path):
    supported_exts = ['.md', '.ipynb', '.html']
    ext = os.path.splitext(path)[1]
    if ext in supported_exts:
        return ext[1:]

def process_folder(path):
    exts = set()
    for file_item in os.listdir():
        ext = get_file_type(file_item)
        if ext:
            exts.add(ext)
    if not len(exts) > 1:
        return exts[0]
    elif not exts:
        print("No suppoted files found in given folder", path)
        sys.exit(1)

def process_file(path, iscode, type):
    filename = os.path.basename(path)

    if type == 'md':
        md_to_html.convert_and_copy_to_blog(path)
    elif type == 'ipynb':
        ipynb_to_html.convert_and_copy_to_blog(path)
    elif type == 'html':
        html_file_path = os.path.join(BLOG_POSTS_DIR, filename)
        shutil.copyfile(path, html_file_path)

    add_post.add(filename, iscode=iscode)
