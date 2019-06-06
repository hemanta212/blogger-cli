import os.path
from shutil import copyfile, SameFileError

from blogger_cli.converter import ipynb_to_html, md_to_html
from blogger_cli.blog_manager import add_post


def convert_and_copyfiles(ctx):
    file_ext_map = ctx.conversion['file_ext_map']
    html_filenames = []

    convert_file = {
        'md': md_to_html.convert_and_copy_to_blog,
        'ipynb': ipynb_to_html.convert_and_copy_to_blog,
        'html': process_htmlfile
    }

    for file, filetype in file_ext_map.items():
        ctx.vlog("Processing the file", file, "filetype:", filetype)
        converter = convert_file[filetype]
        html_filename = converter(ctx, file)
        html_filenames.append(html_filename)

    return html_filenames


def process_htmlfile(ctx, html_file):
    destination_dir = ctx.conversion['destination_dir']
    html_filename = os.path.basename(html_file)
    html_file_path = os.path.join(destination_dir, html_filename)
    ctx.vlog("copying basic html file to", html_file_path)
    try:
        copyfile(html_file, html_file_path)
    except:
        pass
    return html_filename

