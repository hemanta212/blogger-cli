#!/usr/bin/env python

import os
from shutil import copyfile
import jinja2
import markdown

BLOG_POSTS_DIR = os.path.expanduser('~/hemanta212.github.io/blog')


def convert_and_copy_to_blog(md_file):
    md_file_path = os.path.abspath(os.path.expanduser(md_file))
    html_body = convert(md_file_path)
    write_html_and_md(md_file_path, html_body)


def convert(md_file_path):
    with open(md_file_path, 'r', encoding='utf8') as rf:
        md = rf.read()

    extensions = ['extra', 'smarty']
    html = markdown.markdown(md, extensions=extensions, output_format='html5')
    with open('tmp.html', 'w') as wf:
        wf.write(html)

    return html


def write_html_and_md(md_file_path, html_body):
    md_filename = os.path.basename(md_file_path)
    html_filename = md_filename.replace('.md', '.html')
    html_file_path = os.path.join(BLOG_POSTS_DIR, html_filename)
    new_md_file_path = os.path.join(BLOG_POSTS_DIR, md_filename)

    with open(html_file_path, 'w', encoding='utf8') as wf:
        wf.write(html_body)
        print("File written", html_file_path)

    copyfile(md_file_path, new_md_file_path)
    return html_filename

if __name__ == '__main__':
    file = input('file-> ')
    convert(file)
