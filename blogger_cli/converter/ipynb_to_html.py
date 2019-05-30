import os
from shutil import copyfile, SameFileError

from nbconvert import HTMLExporter
import nbformat
from traitlets.config import Config as TraitletsConfig


def convert_and_copy_to_blog(ipynb_file, destination_dir):
    ipynb_file_path = os.path.abspath(os.path.expanduser(ipynb_file))
    html_body = convert(ipynb_file_path)
    html_filename  = write_html_and_ipynb(ipynb_file_path, html_body, destination_dir)
    return html_filename


def convert(ipynb_file):
    with open(ipynb_file, 'r', encoding='utf8') as rf:
        ipynb_content = rf.read()

    html_exporter = gen_exporter()
    nb = nbformat.reads(ipynb_content, as_version=4)
    (body, __) = html_exporter.from_notebook_node(nb)
    html = make_html_responsive(body)
    return html


def write_html_and_ipynb(ipynb_file_path, html_body, destination_dir):
    ipynb_filename = os.path.basename(ipynb_file_path)
    html_filename = ipynb_filename.replace('.ipynb', '.html')
    html_file_path = os.path.join(destination_dir, html_filename)
    new_ipynb_file_path = os.path.join(destination_dir, ipynb_filename)

    with open(html_file_path, 'w', encoding='utf8') as wf:
        wf.write(html_body)
        print("File written", html_file_path)

    try:
        copyfile(ipynb_file_path, new_ipynb_file_path)
    except SameFileError:
        pass

    return html_filename



def gen_exporter():
    c = TraitletsConfig()
    c.htmlexporter.preprocessors = [
        'nbconvert.preprocessors.extractoutputpreprocessor']
    # create the new exporter using the custom config
    html_exporter = HTMLExporter(config=c)
    html_exporter.template_file = 'basic'
    return html_exporter


def make_html_responsive(html_body):
    html_body = html_body.replace("img src", "img width='100%' src")
    html_body = html_body.replace(" rendered_html", "")
    html_body = html_body.replace(".rendered_html{overflow-x:auto",
                        ".rendered_html{overflow-x:auto;overflow-y: hidden;")
    html_body = html_body.replace("#notebook{font-size:14px;line-height:20px;",
                        "#notebook{font-size:20px;line-height:29px;")
    html_body = html_body.replace("div.text_cell_render{outline:0;resize:none;width:inherit;border-style:none;padding:.5em .5em .5em .4em;color:#000;","div.text_cell_render{outline:0;resize:none;width:inherit;border-style:none;padding:.5em .5em .5em .4em;color:#777;")

    return html_body

