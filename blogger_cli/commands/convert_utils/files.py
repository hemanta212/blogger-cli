import os.path
from shutil import copyfile

from blogger_cli.converter import ipynb_to_html, md_to_html
from blogger_cli.blog_manager import add_post


def gen_file_ext_map(ctx, exclude_html):
    files = ctx.files_being_converted
    file_ext_map = {}

    if exclude_html:
        ctx.SUPPORTED_EXTENSIONS.remove('html') i

    for file in files:
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


def convert_and_copyfiles(ctx, file_ext_map, destination_dir):
    ctx.vlog("Processing the file", file, "filetype:", filetype)

    convert_file = {
        'md': md_to_html.convert_and_copy_to_blog,
        'ipynb': ipynb_to_html.convert_and_copy_to_blog,
        'html': process_htmlfile
    }

    html_filenames = []

    for file, filetype in file_ext_map.items():
        converter = convert_file[filetype]
        html_filename = converter(file, destination_dir)
        ctx.vlog("Succesfully converted", html_filename,
                "adding to blog as iscode=")
        html_filenames.append(html_filename)

    return html_filenames


def process_htmlfile(filename, destination_dir):
    html_filename = os.path.basename(filename)
    html_file_path = os.path.join(destination_dir, html_filename)
    copyfile(filename, html_file_path)
    return html_filename

