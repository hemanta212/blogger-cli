import os
import sys
import shutil
import click

from blogger_cli.converter import ipynb_to_html, md_to_html
from blogger_cli.blog_manager import add_post
from blogger_cli.cli import pass_context

BLOG_POSTS_DIR = os.path.normpath(os.path.expanduser(
    '~/hemanta212.github.io/blog'))

SUPPORTED_EXTENSIONS = ['md', 'ipynb', 'html']

@click.command('convert', short_help='Convert files to html')
@click.argument('path', nargs=-1, required=True,
                type=click.Path(exists=True))
@click.option('-f', '--file', is_flag=True,
        help="Convert files")
@click.option('-F', '--folder', is_flag=True,
        help="Convert folder")
@click.option('--not-code', 'iscode', is_flag=True, default=True,
        help="Do not add mathjax and code support")
@click.option('--type', 'filetype',
        help="Type of source file eg: md, ipynb, html")
@click.option('-to', 'destination_dir', type=click.Path(exists=True),
    help="Destination for converted files", default=BLOG_POSTS_DIR)
@click.option('-v', '--verbose', is_flag=True,
        help="Enable verbose flag")

@pass_context
def cli(ctx, path, iscode, filetype, file,
         folder, destination_dir, verbose):
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

    if file:
        ctx.vlog("Converting given file", path)
        files = validate_extension(ctx, path, filetype)
        queue_to_process_file(ctx, files, filetype,
                             destination_dir, iscode)
    elif folder:
        ctx.vlog("Processing the folder", path)
        filetype = check_and_ensure_filetype(filetype)
        folder = path[0]
        process_folder(ctx, folder, filetype,
                     destination_dir, iscode)
    else:
        ctx.log("ERROR: Please specify file or folder with -f or -F",
                "\n See blogger convert --help")


def validate_extension(ctx, path, filetype):
    files = path
    if not filetype:
        files = get_supported_files(ctx, path)

    elif filetype not in SUPPORTED_EXTENSIONS:
        ctx.log("Got unexpected file extension", filetype)
        ctx.exit("ERROR: Unsupported type")
    return files

def queue_to_process_file(ctx, files, filetype,
                         destination_dir, iscode):

    for file in files:
        filetype = filetype if filetype is not None else get_file_extension(file)
        process_file(ctx, file, filetype,
                 destination_dir, iscode)


def get_supported_files(ctx, path):
    supported_files = []
    for file in path:
        filetype = get_file_extension(file)
        if filetype not in SUPPORTED_EXTENSIONS:
            ctx.log("Warning: Unsupported type", filetype, "skipping...")
            continue
        else:
            ctx.vlog("Got file", path, "Passing for convertsion")
            supported_files.append(file)
    return supported_files


def get_file_extension(file):
    extension = os.path.splitext(file)[1]
    return extension[1:]


def process_file(ctx, file, filetype,
                 destination_dir, iscode):

    ctx.vlog("Processing the file", file, "filetype:", filetype)
    convert_file = {
        'md': md_to_html.convert_and_copy_to_blog,
        'ipynb': ipynb_to_html.convert_and_copy_to_blog,
        'html': process_htmlfile
    }
    converter = convert_file[filetype]
    html_filename = converter(file, destination_dir)
    ctx.vlog("Succesfully converted", html_filename,
            "adding to blog as iscode=", iscode)
    add_post.add(ctx, html_filename, destination_dir, iscode=iscode)


def process_htmlfile(filename, destination_dir):
    html_filename = os.path.basename(filename)
    html_file_path = os.path.join(destination_dir, html_filename)
    shutil.copyfile(filename, html_file_path)
    return html_filename


def check_and_ensure_filetype(filetype):
    if not filetype:
        filetype = click.prompt("Filetype to convert from")
    if filetype not in SUPPORTED_EXTENSIONS:
        ctx.exit("Invalid type" + filetype)
    return filetype

def process_folder(ctx, folder, filetype, destination_dir, iscode):
    required_files = []
    for file in os.listdir(folder):
        extension = get_file_extension(file)
        if filetype == extension:
          ctx,   required_files.append(file)

    queue_to_process_file(ctx, required_files, filetype,
                         destination_dir, iscode)
