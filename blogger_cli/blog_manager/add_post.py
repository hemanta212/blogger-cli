import os
import jinja2
import shutil
from bs4 import BeautifulSoup as BS
from pkg_resources import resource_string


def add(filename, conversion):
    post_file_path = os.path.join(conversion.destination_dir, filename)
    ctx.vlog("Adding blog post to", post_file_path)
    html_body = read_blog_body(ctx, post_file_path)
    html_page = insert_html_snippets(ctx, html_body, iscode=iscode)
    write_html(ctx, html_page, post_file_path)
    update_posts_index(ctx, html_page, filename, destination_dir)


def read_blog_body(ctx, file_path):
    ctx.vlog("Reading html body", file_path)
    with open(file_path, 'r', encoding='utf8') as rf:
        content = rf.read()
    return content


def get_cli_resource(path):
    file_path = 'resources/' + path
    file_content = resource_string('blogger_cli', file_path)
    return file_content.decode('utf8')


def insert_html_snippets(ctx, body, iscode=None):
    ctx.vlog("Inserting html_snippets as iscode=", iscode)
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


def write_html(ctx, html_page, file_path):
    ctx.vlog("Writing html to blog posts in", file_path)
    with open(file_path, 'w', encoding='utf8') as wf:
        wf.write(html_page)

def update_posts_index(ctx, html_page, filename, destination_dir):
    ctx.vlog("Updating Posts index of post", filename)
    posts_index_path = os.path.join(destination_dir, 'index.html')
    index_dict = parse_index(ctx, posts_index_path)
    blog_title = get_page_title(ctx, html_page)

    if blog_title in index_dict.values():
        print("WARNING:Duplicate title.",
            "Two blogs with same title!")

    ctx.vlog("Appending to index dict", filename,
             ': ', blog_title)
    index_dict[filename] = blog_title
    index_layout = get_cli_resource('common/index.html')
    index_page = jinja2.Template(index_layout).render(blog_info=index_dict)

    with open(posts_index_path, 'w', encoding='utf8') as wf:
        wf.write(index_page)
        print("index updated", posts_index_path)


def get_page_title(ctx, page):
    soup = BS(page, 'html.parser')
    try:
        title = soup.find_all('h1')[0].contents[0]
        if title is None:
            title = "Hemanta Sharma"
    except IndexError:
        title = "Hemanta Sharma"

    ctx.vlog("Got page title as::", title)
    return title


def parse_index(ctx, index, div_class='blog_list'):
    ctx.vlog("Parsing the index file in", index)
    try:
        with open(index, 'rb') as rf:
            content = rf.read()
    except FileNotFoundError:
        ctx.log("No index.html file. Is this a blog?")
        ctx.exit("ERROR: NO INDEX PAGE")


    try:
        soup = BS(content, 'html.parser')
        list_div = soup.find('div', class_=div_class)
        li_list = list_div.find_all('li')
        my_dict = {}
    except AttributeError:
        ctx.exit("ERROR: INVALID INDEX FILE")

    for link in li_list:
        file_link = link.a['href']
        blog_title = link.a.text
        my_dict[file_link] = blog_title

    ctx.vlog("Got index dict::\n", my_dict)
    return my_dict
