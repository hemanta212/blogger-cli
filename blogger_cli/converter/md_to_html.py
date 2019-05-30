#!/usr/bin/env python

import os
from shutil import copyfile, SameFileError
import jinja2
import markdown


def convert_and_copy_to_blog(md_file, destination_dir):
    md_file_path = os.path.abspath(os.path.expanduser(md_file))
    html_body = convert(md_file_path)
    html_filename = write_html_and_md(md_file_path, html_body,
                                    destination_dir)
    return html_filename


def convert(md_file_path):
    with open(md_file_path, 'r', encoding='utf8') as rf:
        md = rf.read()

    extensions = ['extra', 'smarty']
    html = markdown.markdown(md, extensions=extensions, output_format='html5')
    return html


def write_html_and_md(md_file_path, html_body, destination_dir):
    md_filename = os.path.basename(md_file_path)
    html_filename = md_filename.replace('.md', '.html')
    html_file_path = os.path.join(destination_dir, html_filename)
    new_md_file_path = os.path.join(destination_dir, md_filename)

    with open(html_file_path, 'w', encoding='utf8') as wf:
        wf.write(html_body)
        print("File written", html_file_path)

    try:
        copyfile(md_file_path, new_md_file_path)
    except  SameFileError:
        pass

    return html_filenam

