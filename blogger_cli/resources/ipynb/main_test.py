'''
ipynb to html converter script
'''
import os
import jinja2

from bs4 import BeautifulSoup as BS
from nbconvert import HTMLExporter
import nbformat
from traitlets.config import Config as TraitletsConfig

BASIC = True
resource_dir = ''

def convert(notebook_file):
    c = TraitletsConfig()
    c.HTMLExporter.preprocessors = [
        'nbconvert.preprocessors.ExtractOutputPreprocessor']

    # create the new exporter using the custom config
    html_exporter = HTMLExporter(config=c)
    html_exporter = HTMLExporter()

    if BASIC:
        html_exporter.template_file = 'basic'

    nb = nbformat.reads(open(notebook_file, 'r', encoding='utf8').read(), as_version=4)

    (body, __) = html_exporter.from_notebook_node(nb)
    # FIRST between H1 in body
    filename = os.path.basename(notebook_file)
    filename = filename.replace('.ipynb', '.html')

    soup = BS(body, 'html.parser')
    try:
        title = soup.find_all('h1')[0].contents[0]
        if title is None:
            title = "Hemanta Sharma"
    except IndexError:
        title = "Hemanta Sharma"

    return filename, title, body

def read_file(file):
    path = os.path.join(resource_dir, file)
    with open(path, 'r') as wr:
        content = wr.read()
        return content

def process(body=None, title=None, file=None):
    blog_dir = 'F:/my_projects/hemanta212.github.io/'
    layout = read_file('layout.html')
    css = read_file('css.txt')
    navbar_txt = read_file('navbar.txt')
    mathjax = read_file('mathjax.txt')
    bootstrap_js = read_file('bootstrap_js.txt')
    google_analytics = read_file('google_analytics.txt')
    disqus = read_file('disqus.txt')

    body = body.replace("img src", "img width='100%' src")
    body = body.replace(" rendered_html", "")
    body = body.replace(".rendered_html{overflow-x:auto",
                        ".rendered_html{overflow-x:auto;overflow-y: hidden;")
    body = body.replace("#notebook{font-size:14px;line-height:20px;",
                        "#notebook{font-size:20px;line-height:29px;")
    body = body.replace("div.text_cell_render{outline:0;resize:none;width:inherit;border-style:none;padding:.5em .5em .5em .4em;color:#000;","div.text_cell_render{outline:0;resize:none;width:inherit;border-style:none;padding:.5em .5em .5em .4em;color:#777;")

    navbar_dict = {
        'Home': '../index.html',
        'Blog': 'index.html',
        'Teaching': '../pykancha.html',
        'Projects': '../projects.html/',
    }
    navbar = jinja2.Template(navbar_txt).render(navbar_dict=navbar_dict)

    template = jinja2.Template(layout)
    final = template.render(css=css, google_analytics=google_analytics,
                             bootstrap_js=bootstrap_js, disqus_script=disqus,
                             mathjax_script=mathjax, body=body, navbar=navbar)

    blog_path = 'F:/my_projects/hemanta212.github.io/blog/'
    file_path = os.path.join(blog_path, file)
    with open(file_path, 'w', encoding='utf8') as wf:
        wf.write(final)
        print("File written", file_path)

    # for i, j, k in os.walk(blog_dir):
    #     I = i[len(blog_dir):]
    #     for item in k:
    #         if os.path.splitext(item)[-1] != '.html':
    #             break
    #         path = os.path.join(I, item)
    #         path = path.replace('\\', '/')

    index_dict = parse_index()
    index_dict[file] = title
    with open('index.html', 'r') as in_read:
        content = in_read.read()

    index_page = jinja2.Template(content).render(blog_info = index_dict)
    blog_index_path = 'F:/my_projects/hemanta212.github.io/blog/index.html'
    with open(blog_index_path, 'w') as wf:
        wf.write(index_page)
        print("index updated", blog_index_path)
    return final


def parse_index(index= None, list_div=None):
    if not index:
        index = 'F:/my_projects/hemanta212.github.io/blog/index.html'
    if not list_div:
        list_div = 'blog_list'

    with open(index, 'rb') as rf:
        content = rf.read()

    soup = BS(content, 'html.parser')
    list_div = soup.find('div', class_=list_div)
    li_list = list_div.find_all('li')
    my_dict = {}
    for link in li_list:
        file_link = link.a['href']
        title = link.a.text
        my_dict[file_link] = title

    return my_dict

if __name__ == '__main__':
    file = input('Input File:> ')
    filename, title, body = convert(file)
    process(file=filename, body=body, title=title)
