import os.path
from shutil import copyfile, SameFileError

from blogger_cli.converter import ipynb_to_html, md_to_html
from blogger_cli.blog_manager import add_post


def convert_and_copyfiles(conversion):
    convert_file = {
        'md': md_to_html.convert_and_copy_to_blog,
        'ipynb': ipynb_to_html.convert_and_copy_to_blog,
        'html': process_htmlfile
    }
    html_filenames = []
    for file, filetype in conversion.file_ext_map.items():
        conversion.vlog("Processing the file", file, "filetype:", filetype)
        converter = convert_file[filetype]
        html_filename = converter(file, conversion)
        html_filenames.append(html_filename)

    return html_filenames


def process_htmlfile(filename, destination_dir):
    html_filename = os.path.basename(filename)
    html_file_path = os.path.join(destination_dir, html_filename)
    try:
        copyfile(filename, html_file_path)
    except:
        pass
    return html_filename

