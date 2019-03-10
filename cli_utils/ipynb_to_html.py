'''
ipynb to html converter script 
'''
from builtins import open
from bs4 import BeautifulSoup
from nbconvert import HTMLExporter
import nbformat
from traitlets.config import Config as TraitletsConfig

BASIC = True


def convert(notebook_file):
    c = TraitletsConfig()
    c.HTMLExporter.preprocessors = [
        'nbconvert.preprocessors.ExtractOutputPreprocessor']

    # create the new exporter using the custom config
    html_exporter = HTMLExporter(config=c)
    html_exporter = HTMLExporter()

    if BASIC:
        html_exporter.template_file = 'basic'

    nb = nbformat.reads(open(notebook_file, 'r').read(), as_version=4)

    (body, __) = html_exporter.from_notebook_node(nb)
    # FIRST between H1 in body
    soup = BeautifulSoup(body, 'html.parser')
    try:
        title = soup.find_all('h1')[0].contents[0]
        if title is None:
            title = "Pykancha"
    except IndexError:
        title = "PYKANCHA"

    if BASIC:
        with open('template.html', 'r') as rf:
            html = rf.read()
            body = '''{0}'''.format(html)

    # Put social media icons
    body = body.replace("img src", "img width='100%' src")

    body = body.replace(" rendered_html", "")
    body = body.replace(".rendered_html{overflow-x:auto",
                        ".rendered_html{overflow-x:auto;overflow-y: hidden;")
    body = body.replace("#notebook{font-size:14px;line-height:20px;",
                        "#notebook{font-size:20px;line-height:29px;")
    body = body.replace("div.text_cell_render{outline:0;resize:none;width:inherit;border-style:none;padding:.5em .5em .5em .4em;color:#000;",
                        "div.text_cell_render{outline:0;resize:none;width:inherit;border-style:none;padding:.5em .5em .5em .4em;color:#777;")

    html_file = notebook_file.replace(".ipynb", ".html")
    with open(html_file, 'w') as html_file_writer:
        html_file_writer.write(body)
