import os
import jinja2
import shutil
from bs4 import BeautifulSoup as BS
from pkg_resources import resource_string

BLOG_POSTS_DIR = os.path.expanduser('~/hemanta212.github.io/blog')

def add(filename, iscode=None):
    post_file_path = os.path.join(BLOG_POSTS_DIR, filename)
    html_body = read_blog_body(post_file_path)
    html_page = insert_html_snippets(html_body, iscode=iscode)
    write_html(html_page, post_file_path)
    update_posts_index(html_page, filename)


def read_blog_body(file_path):
    with open(file_path, 'r') as rf:
        content = rf.read()
    return content


def get_cli_resource(path):
    file_path = 'resources/' + path
    file_content = resource_string('blogger_cli', file_path)
    return file_content.decode('utf8')


def insert_html_snippets(body, iscode=None):
    layout = get_cli_resource('ipynb/layout.html')
    navbar_layout = get_cli_resource('common/navbar.html')
    bootstrap_js = get_cli_resource('ipynb/bootstrap_js.html')
    google_analytics = get_cli_resource('common/google_analytics.html')
    disqus = get_cli_resource('common/disqus.html')

    if iscode:
        css = get_cli_resource('ipynb/css.html')
        mathjax = get_cli_resource('ipynb/mathjax.html')
    else:
        css = ''
        mathjax=''

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


def write_html(html_page, file_path):
    with open(file_path, 'w') as wf:
        wf.write(html_page)

def update_posts_index(html_page, filename):
    posts_index_path = BLOG_POSTS_DIR + '/index.html'
    index_dict = parse_index(posts_index_path)
    blog_title = get_page_title(html_page)

    if blog_title in index_dict.values():
        print("WARNING:Duplicate title.",
            "Two blogs with same title!")

    index_dict[filename] = blog_title
    index_layout = get_cli_resource('common/index.html')
    index_page = jinja2.Template(index_layout).render(blog_info=index_dict)

    with open(posts_index_path, 'w') as wf:
        wf.write(index_page)
        print("index updated", posts_index_path)



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

