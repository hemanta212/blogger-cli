import json
import os
from collections import OrderedDict
from pathlib import Path

import jinja2
from bs4 import BeautifulSoup as BS
from pkg_resources import resource_string

from blogger_cli.blog_manager.add_post_meta import save_post_meta


def add(ctx, filename_meta):
    filename, meta = Path(filename_meta[0]), filename_meta[1]
    ctx.log(":: Resolving", filename)
    destination_dir = Path(ctx.conversion["destination_dir"])
    file_path = destination_dir / filename
    topic = os.path.dirname(str(filename))
    meta["topic"] = topic

    snippet = get_snippet_content_map(ctx, meta)
    snippet["link"] = str(filename)
    html_page = insert_html_snippets(ctx, file_path, meta, snippet)
    ctx.log(":: Writing finished html to", filename)
    file_path.write_text(html_page, encoding="utf-8")
    update_posts_index(ctx, snippet, meta)
    save_post_meta(ctx, snippet, meta)


def get_snippet_content_map(ctx, meta):
    templates_dir = ctx.conversion.get("templates_dir")
    snippet_names = [
        "layout",
        "disqus",
        "css",
        "li_tag",
        "google_analytics",
        "navbar_data",
        "navbar",
        "js",
        "mathjax",
        "light_theme",
        "dark_theme",
    ]

    snippet_content_map = {}

    for snippet in snippet_names:
        file_name = snippet + ".html"
        file_content = get_internal_resource(file_name)
        snippet_content_map[snippet] = file_content

    if templates_dir:
        template_files = Path(templates_dir).glob("*")
        all_filenames = [i.resolve() for i in template_files if i.is_file()]
        html_filenames = [i for i in all_filenames if i.suffix == ".html"]

        for file in html_filenames:
            custom_snippet = os.path.splitext(str(file.name))[0]
            snippet_content_map[custom_snippet] = file.read_text(encoding="utf-8")

    resolve_templates(ctx, snippet_content_map, meta)
    return snippet_content_map


def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as rf:
        content = rf.read()
    return content


def get_internal_resource(file_name):
    internal_resource_path = "resources/" + file_name
    file_content = resource_string("blogger_cli", internal_resource_path)
    return file_content.decode("utf-8")


def insert_html_snippets(ctx, file_path, meta, snippet_content_map):
    iscode = ctx.conversion["iscode"]
    ctx.log(":: Inserting html_snippets to file")
    html_body = file_path.read_text(encoding="utf-8")

    ctx.vlog(":: iscode =", iscode)
    if not iscode:
        snippet_content_map["css"] = ""
        snippet_content_map["mathjax"] = ""
        snippet_content_map["dark_theme"] = ""
        snippet_content_map["light_theme"] = ""

    snippet_content_map["body"] = html_body
    snippet_content_map["title"] = get_page_title(ctx, html_body)

    layout = snippet_content_map["layout"]
    template = jinja2.Template(layout)

    snippet_content_map.pop("layout")
    final_page = template.render(snippet=snippet_content_map, meta=meta)
    if iscode:
        html_page = insert_prettyprint_class(ctx, final_page)

    return html_page


def insert_prettyprint_class(ctx, html_page):
    soup = BS(html_page, features="html.parser")
    pre_tags = soup.find_all("pre")
    if not pre_tags:
        ctx.log(":: WARNING: No pre tags found in code")
        return html_page

    for pre_tag in pre_tags:
        pre_tag["class"] = "prettyprint"

    return soup.prettify(formatter="html")


def resolve_templates(ctx, snippet_content_map, meta):
    config = dict()
    blog = ctx.current_blog
    topic = meta.get("topic")
    navbar_dict = get_navbar_dict(ctx, snippet_content_map, topic)
    layout_renderer_map = {
        "disqus": config,
        "google_analytics": config,
        "navbar": navbar_dict,
    }
    config_names = ["disqus_username", "google_analytics_id"]
    for config_name in config_names:
        config_key = blog + ":" + config_name
        config[config_name] = ctx.config.read(key=config_key)

    exclude_snippet = ["layout", "li_tag"]
    for snippet, content in snippet_content_map.items():
        if snippet not in exclude_snippet:
            renderer = layout_renderer_map.get(snippet)
            content_template = jinja2.Template(content)
            html_snippet = content_template.render(config=renderer, meta=meta)
            snippet_content_map[snippet] = html_snippet


def get_navbar_dict(ctx, snippet_content_map, topic):
    try:
        navbar_dict = json.loads(
            snippet_content_map["navbar_data"], object_pairs_hook=OrderedDict
        )
    except Exception as E:
        ctx.log(
            ":: Could not parse your custom navbar", E, "ERROR: INVALID NAVBAR TEMPLATE"
        )
        raise SystemExit()

    if topic:
        for nav_topic, nav_link in navbar_dict.items():
            nav_link = "../" + nav_link
            navbar_dict[nav_topic] = nav_link

    return navbar_dict


def get_page_title(ctx, page):
    current_blog = ctx.current_blog
    filter_ = ctx.config.read(key=current_blog + ":filter_post_without_title")
    if filter_ in ["true", "True"]:
        ctx.log(":: Filtering this post as it doesnot have title")
        current_blog = ""

    soup = BS(page, "html.parser")
    try:
        title = soup.find_all("h1")[0].contents[0]
        if title is None:
            title = current_blog
    except IndexError:
        title = current_blog

    title = title.strip()
    ctx.log(":: Got page title as", title)
    return title


def update_posts_index(ctx, snippet_content_map, meta):
    post_li_tag_div = prepare_post_list(meta, snippet_content_map)
    destination_dir = ctx.conversion["destination_dir"]
    index_path = os.path.join(destination_dir, "index.html")
    index_div_class = "posts_list"
    index_class = ctx.config.read(key=ctx.current_blog + ": index_div_name")
    if index_class:
        index_div_class = index_class

    topic = meta["topic"]

    if not os.path.exists(index_path):
        ctx.vlog(":: Cannot find index file in", index_path)
        ctx.log("WARNING: NO INDEX FILE. SEE blogger export --help")
        return None

    soup = BS(read_file(index_path), features="html.parser")
    posts_list_div = soup.find("div", class_=index_div_class)

    if not posts_list_div:
        ctx.log(":: Cannot update blog index! No div with", index_div_class, "class")
        ctx.log("WARNING: INVALID INDEX.", index_path)
        return None

    ctx.log(":: Updating index file at", index_path)
    if topic and post_li_tag_div:
        update_under_topic(posts_list_div, post_li_tag_div, topic)
        ctx.log(":: Linking under topic", topic)
    elif post_li_tag_div:
        update_without_topic(posts_list_div, post_li_tag_div)

    snippet = snippet_content_map
    ctx.log(":: File link and title", snippet["link"], "->", snippet["title"])

    soup = filter_invalid_index_links(ctx, soup, destination_dir)
    with open(index_path, "w", encoding="utf-8") as wf:
        wf.write(soup.prettify(formatter="html"))

    ctx.log("Index successfully updated\n")


def update_under_topic(posts_list_div, post_li_tag_div, topic):
    div_topic = "meta-" + topic
    topic_tag = posts_list_div.find("div", class_=div_topic)
    if topic_tag:
        file_link = post_li_tag_div.ul.li.a["href"]
        topic_tag = check_and_remove_duplicate_tag(topic_tag, file_link)
        ul_tag = post_li_tag_div.ul.extract()
        topic_tag.append(ul_tag)

    else:
        post_li_tag_div["class"] = div_topic
        h3_soup = BS("<h3> " + topic + "</h3>\n", features="html.parser")
        h3_tag = h3_soup.find("h3")
        post_li_tag_div.insert(0, h3_tag)
        posts_list_div.insert(0, post_li_tag_div)


def update_without_topic(posts_list_div, post_li_tag):
    file_link = post_li_tag.ul.li.a["href"]
    posts_list_div = check_and_remove_duplicate_tag(posts_list_div, file_link)
    li_tag_ul = post_li_tag.ul.extract()
    posts_list_div.insert(0, li_tag_ul)


def prepare_post_list(meta, snippet):
    if not snippet["title"]:
        return None

    li_tag_layout = snippet["li_tag"]
    li_tag_template = jinja2.Template(li_tag_layout)
    li_tag_html = li_tag_template.render(meta=meta, snippet=snippet)

    li_tag = BS(li_tag_html, features="html.parser").find("li")
    new_div = """\
<div>
    <ul>

    </ul>
</div>"""

    new_div_tag = BS(new_div, features="html.parser").find("div")
    new_div_tag.ul.append(li_tag)
    return new_div_tag


def check_and_remove_duplicate_tag(div_tag, file_link):
    try:
        ul_tags = div_tag.find_all("ul")
    except AttributeError:
        return div_tag

    for ul_tag in ul_tags:
        li_tag_link = ul_tag.li.a["href"]
        if li_tag_link == file_link:
            ul_tag.decompose()

    return div_tag


def filter_invalid_index_links(ctx, soup, blog_posts_dir):
    ctx.log(":: Checking validity of existing index links...")
    blog = ctx.current_blog
    posts_list_div = ctx.config.read(key=blog + ":index_div_name")
    if not posts_list_div:
        posts_list_div = "posts_list"

    posts_list = soup.find("div", class_=posts_list_div)
    ul_tags = posts_list.find_all("ul")
    for ul_tag in ul_tags:
        try:
            href_data = ul_tag.li.a["href"]
            if (
                href_data.startswith("http:")
                or href_data.startswith("file:")
                or href_data.startswith("data:")
            ):
                raise ValueError
        except Exception as E:
            ctx.vlog(E)
            href_data = None

        if href_data:
            full_path = os.path.join(blog_posts_dir, href_data)
            if not os.path.exists(full_path):
                ctx.log(":: WARNING! Deleting invalid index path", full_path)
                ul_tag.decompose()

    ctx.log(":: Index links checking \ Done!")
    return soup
