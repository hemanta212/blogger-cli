'''
ipynb to html converter script

[TODO} MAYBE TITLE ERROR CAN BE RESOLVED BY PASSING BODY TO get_page_title
'''
import os
import sys
import jinja2
import shutil

from bs4 import BeautifulSoup as BS
from nbconvert import HTMLExporter
import nbformat
from traitlets.config import Config as TraitletsConfig
from pkg_resources import resource_string


BLOG_POSTS_DIR = os.path.expanduser('~/hemanta212.github.io/blog')


def generate_html(ipynb_file):
    ipynb_file_path = os.path.abspath(os.path.expanduser(ipynb_file))
    html_body = convert_to_html(ipynb_file_path)
    html_page = insert_html_snippets(html_body)
    html_file_name = write_html_and_ipynb(ipynb_file_path, html_page)
    update_posts_index(html_page, html_file_name)


def convert_to_html(notebook_file):
    c = TraitletsConfig()
    c.HTMLExporter.preprocessors = [
        'nbconvert.preprocessors.ExtractOutputPreprocessor']
    # create the new exporter using the custom config
    html_exporter = HTMLExporter(config=c)
    html_exporter.template_file = 'basic'

    with open(notebook_file, 'r', encoding='utf8') as rf:
        ipynb_content = rf.read()

    nb = nbformat.reads(ipynb_content, as_version=4)
    body, __ = html_exporter.from_notebook_node(nb)

    # Make body responsive or mobile friendly
    body = body.replace("img src", "img width='100%' src")
    body = body.replace(" rendered_html", "")
    body = body.replace(".rendered_html{overflow-x:auto",
                        ".rendered_html{overflow-x:auto;overflow-y: hidden;")
    body = body.replace("#notebook{font-size:14px;line-height:20px;",
                        "#notebook{font-size:20px;line-height:29px;")
    body = body.replace("div.text_cell_render{outline:0;resize:none;width:inherit;border-style:none;padding:.5em .5em .5em .4em;color:#000;","div.text_cell_render{outline:0;resize:none;width:inherit;border-style:none;padding:.5em .5em .5em .4em;color:#777;")

    return body


def insert_html_snippets(body=None, title=None, file=None):
    layout = get_resource('ipynb/layout.html')
    css = get_resource('ipynb/css.html')
    navbar_layout = get_resource('common/navbar.html')
    mathjax = get_resource('ipynb/mathjax.html')
    bootstrap_js = get_resource('ipynb/bootstrap_js.html')
    google_analytics = get_resource('common/google_analytics.html')
    disqus = get_resource('common/disqus.html')

    navbar_dict = {
        'Home': '../index.html',
        'Blog': 'index.html',
        'Teaching': '../pykancha.html',
        'Projects': '../projects.html/',
    }
    navbar = jinja2.Template(navbar_layout).render(navbar_dict=navbar_dict)
    template = jinja2.Template(layout)
    final_page = template.render(css=css, google_analytics=google_analytics,
                             bootstrap_js=bootstrap_js, disqus_script=disqus,
                             mathjax_script=mathjax, body=body, navbar=navbar)
    return final_page


def update_posts_index(html_page, html_filename):
    posts_index_path = BLOG_POSTS_DIR + '/index.html'
    index_dict = parse_index(posts_index_path)
    blog_title = get_page_title(html_page)

    if blog_title in index_dict.values():
        print("WARNING:Duplicate title.",
            "Two blogs with same title!")

    index_dict[html_filename] = blog_title
    index_layout = get_resource('common/index.html')
    index_page = jinja2.Template(index_layout).render(blog_info=index_dict)

    with open(posts_index_path, 'w') as wf:
        wf.write(index_page)
        print("index updated", posts_index_path)


def write_html_and_ipynb(ipynb_file_path, html_page):
    ipynb_filename = os.path.basename(ipynb_file_path)
    html_filename = ipynb_filename.replace('.ipynb', '.html')
    html_file_path = os.path.join(BLOG_POSTS_DIR, html_filename)
    new_ipynb_file_path = os.path.join(BLOG_POSTS_DIR, ipynb_filename)

    with open(html_file_path, 'w', encoding='utf8') as wf:
        wf.write(html_page)
        print("File written", html_file_path)

    shutil.copyfile(ipynb_file_path, new_ipynb_file_path)
    return html_filename


def get_resource(path):
    file_path = 'resources/' + path
    file_content = resource_string('blogger_cli', file_path)
    return file_content.decode('utf8')


def get_page_title(page):
    soup = BS(page, 'html.parser')
    try:
        title = soup.find_all('h1')[0].contents[0]
        if title is None:
            title = "Hemanta Sharma"
    except IndexError:
        title = "Hemanta Sharma"
    return title


def parse_index(index, div_class='blog_list'):
    with open(index, 'rb') as rf:
        content = rf.read()

    soup = BS(content, 'html.parser')
    list_div = soup.find('div', class_=div_class)
    li_list = list_div.find_all('li')
    my_dict = {}

    for link in li_list:
        file_link = link.a['href']
        blog_title = link.a.text
        my_dict[file_link] = blog_title

    return my_dict


if __name__ == '__main__':
    file = input('Input File:> ')
    generate_html(file)
