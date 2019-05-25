import os
import sys
import shutil
import click

from blogger_cli.converter import ipynb_to_html, md_to_html
from blogger_cli.blog_manager import add_post
from blogger_cli.cli import pass_context

BLOG_POSTS_DIR = os.path.expanduser('~/hemanta212.github.io/blog')

@click.command('convert', short_help='Convert files to html')
@click.argument('path', nargs=-1, required=True,
                type=click.Path(exists=True))
@click.option('-f', '--file', is_flag=True, )
@click.option('-F', '--folder', is_flag=True)
@click.option('--not-code', 'iscode', is_flag=True, default=True)
@click.option('-t', '--type')
@click.option('-v', '--verbose', is_flag=True)

@pass_context
def cli(ctx, path, iscode, type, file, folder, verbose):
    """Convert diffrent file format to html
   Usage:

    For files::
    blogger convert -f filename.ipynb
    blogger convert -f file1 file2 file3
    blogger convert -f filename --not-code

    For folder::
    blogger convert -F folder_with_files --type html
    blogger convert -F folder1 folder2 --type md --notcode

    """
    ctx.verbose = verbose

    if file:
        ctx.vlog("Processing the file", path)
        validate_file(path, type)
        process_file(path, iscode, type)
    elif folder:
        ctx.vlog("Processing the folder", path)
        validate_folder(path, type)
        process_folder(path, type)
    else:
        ctx.log("ERROR: Please specify file or folder with -f or -F",
                "\n See blogger convert --help")


def validate_filetype(path, type):
    supported_exts = ['.md', '.ipynb', '.html']
    if type not in supported_exts:
        ctx.log("ERROR: Unsupported type", type)
        ctx.exit()

    elif not type:
        gsupported_files = get_supported_files(path)

def get_supported_files(path):
    supported_files = tuple()
    for file in path:
        type = get_file_type(file)
        if type not in supported_ext:
            ctx.log("Warning: Unsupported type", ext, "skipping...")
            continue
         else:
            ctx.vlog("Got file", path, "Passing for convertsion")
            supported_files.add(file)

def get_file_type(file):
    ext = os.path.splitext(file)[1]
    return ext[1:]

def process_folder(path, type):
    if not type:
        ctx.log("Error:No type given, type option required for folders")

    for file in os.listdir(path):
        cext = file.split(ext


def process_file(file, iscode, type):
    convert_file = {
        'md': md_to_html.convert_and_copy_to_blog,
        'ipynb': ipynb_to_html.convert_and_copy_to_blog,
        'html': process_htmlfile
    }
    converter = convert_file[type]
    html_filename = converter(file)
    add_post.add(html_filename, iscode=iscode)


def process_htmlfile(path):
    html_filename = os.path.basename(path)
    html_file_path = os.path.join(BLOG_POSTS_DIR, html_filename)
    shutil.copyfile(path, html_file_path)
    return html_filename
