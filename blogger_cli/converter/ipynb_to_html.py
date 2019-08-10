import os
import json
from shutil import copyfile
from collections import OrderedDict

import jinja2
from bs4 import BeautifulSoup as BS
from nbconvert import HTMLExporter
import nbformat
from traitlets.config import Config as TraitletsConfig

from blogger_cli.converter.extractor import (
        extract_meta_format, replace_ext, extract_topic,
        extract_main_and_meta_from_file_content, extract_and_write_static
        )


def convert_and_copy_to_blog(ctx, ipynb_file):
    ipynb_file_path = os.path.abspath(os.path.expanduser(ipynb_file))
    html_body, meta = convert_to_html(ctx, ipynb_file_path)
    html_filename_meta = write_html_and_ipynb(ctx, ipynb_file_path,
                                                html_body, meta)
    return html_filename_meta


def convert_to_html(ctx, ipynb_file_path):
    html_exporter = gen_exporter()
    ipynb_data, metadata = extract_main_and_meta(ctx, ipynb_file_path)
    nb = nbformat.reads(ipynb_data, as_version=4)
    (body, __) = html_exporter.from_notebook_node(nb)
    return body, metadata


def gen_exporter():
    config = TraitletsConfig()
    config.htmlexporter.preprocessors = [
        'nbconvert.preprocessors.extractoutputpreprocessor']
    html_exporter = HTMLExporter(config=config)
    html_exporter.template_file = 'basic'
    return html_exporter


def extract_main_and_meta(ctx, ipynb_file_path):
    blog = ctx.current_blog
    metadata = OrderedDict()
    delete_ipynb_meta = ctx.config.read(key=blog + ':delete_ipynb_meta')
    ctx.written_ipynb = False
    with open(ipynb_file_path, 'r', encoding='utf-8') as rf:
        ipynb_data = rf.read()

    nbdata_file_path = replace_ext(ipynb_file_path, '.nbdata')
    if os.path.exists(nbdata_file_path):
        ctx.vlog(":: Reading nbdata file", nbdata_file_path)
        with open(nbdata_file_path, 'r', encoding='utf-8') as rf:
            nbdata_content = rf.read()

        __, metadata = extract_main_and_meta_from_file_content(
                                            ctx, nbdata_content)
    if not metadata:
        ctx.vlog(":: Extracting meta from file", ipynb_file_path)
        ipynb_data, metadata = extract_main_and_meta_from_ipynb(
                                                ctx, ipynb_data)

        if metadata and not delete_ipynb_meta in ['false', 'False']:
            ipynb_filename = os.path.basename(ipynb_file_path)
            topic = extract_topic(ctx, metadata)
            blog_post_dir = get_blog_post_dir(ctx, topic)
            new_ipynb_file_path = os.path.join(blog_post_dir, ipynb_filename)

            ctx.log(":: Deleting meta from ipynb_file", new_ipynb_file_path )
            with open(new_ipynb_file_path, 'w', encoding='utf-8') as wf:
                ipynb_dict = json.loads(ipynb_data)
                json.dump(ipynb_dict, wf, indent=2)
            ctx.written_ipynb = True

    return ipynb_data, metadata


def extract_main_and_meta_from_ipynb(ctx, ipynb_data):
    metadata = OrderedDict()
    ipynb_dict = json.loads(ipynb_data)
    meta_start, meta_end = extract_meta_format(ctx)

    try:
        raw_meta = ipynb_dict['cells'][0].get('source')
        if not raw_meta:
            ctx.log(':: Metadata, The first cell is empty!')

        meta_list = [str(i).strip() for i in raw_meta]
        try:
            first_mark = meta_list.index(meta_start)
            second_mark = meta_list.index(meta_end)
        except ValueError:
            ctx.log(':: Meta tags:', meta_start, meta_end, "Not found")
            return ipynb_data, metadata

        meta = [i for i in meta_list[first_mark+1:second_mark] if i]
        for key_value in meta:
            key, value = key_value.split(':')
            if value:
                metadata[key.strip()] = value.strip()

        del ipynb_dict['cells'][0]
        ipynb_data = json.dumps(ipynb_dict)

    except Exception as E:
        ctx.log(":: Ipynb file is empty")

    finally:
        ctx.vlog(":: Got metadata", metadata)
        return ipynb_data, metadata


def get_blog_post_dir(ctx, topic):
    destination_dir = ctx.conversion['destination_dir']
    blog_post_dir = os.path.join(destination_dir, topic)
    return blog_post_dir


def write_html_and_ipynb(ctx, ipynb_file_path,  html_body, meta):
    blog = ctx.current_blog
    extract_static = ctx.conversion['extract_static']
    create_nbdata_file = ctx.config.read(key=blog + ':create_nbdata_file')
    topic = extract_topic(ctx, meta)
    ctx.log(":: Got topic,", topic)

    blog_post_dir = get_blog_post_dir(ctx, topic)
    ipynb_filename = os.path.basename(ipynb_file_path)
    html_filename = replace_ext(ipynb_filename, '.html')
    html_file_path = os.path.join(blog_post_dir, html_filename)
    new_ipynb_file_path = os.path.join(blog_post_dir, ipynb_filename)
    ctx.vlog(":: New blog_posts_dir finalized::", blog_post_dir)

    html_topic_filename = os.path.join(topic, html_filename)
    ipynb_topic_filename = replace_ext(html_topic_filename, '.ipynb')
    if not os.path.exists(blog_post_dir):
        os.mkdir(blog_post_dir)

    if extract_static:
        html_body = extract_and_write_static(ctx, html_body, blog_post_dir,
                                            ipynb_topic_filename)

    if meta and not create_nbdata_file in ['false', 'False']:
        create_nbdata_file_in_blog_dir(ctx, meta, new_ipynb_file_path)

    with open(html_file_path, 'w', encoding='utf8') as wf:
        wf.write(html_body)
        ctx.log(":: Converted basic html to", html_file_path)

    if (not ctx.written_ipynb) and (ipynb_file_path != new_ipynb_file_path):
        try:
            copyfile(ipynb_file_path, new_ipynb_file_path)
            ctx.log(":: Copied ipynb file to", new_ipynb_file_path)
        except SameFileError:
            os.remove(new_ipynb_file_path)
            copyfile(ipynb_file_path, new_ipynb_file_path)
            ctx.log(":: Overwriting ipynb file", new_ipynb_file_path)

    return (html_topic_filename, meta)


def create_nbdata_file_in_blog_dir(ctx, meta, file_path):
    meta_string = '''
{{meta_format.start}}
{% for key, value in meta.items() %}
{{key}}: {{value}}
{% endfor %}
{{meta_format.end}}
'''
    meta_start, meta_end = extract_meta_format(ctx)
    meta_format = {
        'start': meta_start,
        'end': meta_end
    }
    meta_template = jinja2.Template(meta_string)
    meta_content = meta_template.render(meta_format=meta_format, meta=meta)
    meta_content = os.linesep.join([s for s in meta_content.splitlines() if s])

    nbdata_file_path = replace_ext(file_path, '.nbdata')
    ctx.log(":: Creating nbdata file", nbdata_file_path)
    with open(nbdata_file_path, 'w', encoding='utf-8') as wf:
        wf.write(meta_content)
