import os
import json
from shutil import copyfile, SameFileError

from bs4 import BeautifulSoup as BS
from nbconvert import HTMLExporter
import nbformat
from traitlets.config import Config as TraitletsConfig

from blogger_cli.converter.extractors import extract_and_write_static


def convert_and_copy_to_blog(ctx, ipynb_file):
    ipynb_file_path = os.path.abspath(os.path.expanduser(ipynb_file))
    meta, html_body = convert(ipynb_file_path)
    html_filename_meta = write_html_and_ipynb(ctx, ipynb_file_path,
                                                html_body, meta)
    return html_filename_meta


def write_html_and_ipynb(ctx, ipynb_file_path,  html_body, meta):
    extract_static = ctx.conversion['extract_static']
    destination_dir = ctx.conversion['destination_dir']

    ipynb_filename = os.path.basename(ipynb_file_path)
    given_topic = ctx.conversion.get('topic')
    topic = given_topic if given_topic else ''
    if topic:
        ctx.log(":: Got topic, ", topic)

    ipynb_filename = os.path.join(topic, ipynb_filename)
    html_filename = ipynb_filename.replace('.ipynb', '.html')
    html_file_path = os.path.join(destination_dir, html_filename)
    new_ipynb_file_path = os.path.join(destination_dir, ipynb_filename)
    new_blog_post_dir = os.path.dirname(html_file_path)
    ctx.vlog("New blog_posts_dir finalized::", new_blog_post_dir)

    if not os.path.exists(new_blog_post_dir):
        os.mkdir(new_blog_post_dir)

    if extract_static:
        html_body = extract_and_write_static(ctx, html_body,
                                            ipynb_filename, new_blog_post_dir)


    with open(html_file_path, 'w', encoding='utf8') as wf:
        wf.write(html_body)
        ctx.log(":: Converted basic html to", html_file_path)

    try:
        copyfile(ipynb_file_path, new_ipynb_file_path)
        ctx.log(":: Copied ipynb file to", new_ipynb_file_path)
    except SameFileError:
        os.remove(new_ipynb_file_path)
        copyfile(ipynb_file_path, new_ipynb_file_path)
        ctx.log(":: Overwriting ipynb file", new_ipynb_file_path)

    return (html_filename, meta)


def extract_meta_and_main(ctx, ipynb_data):
    metadata = ''
    meta_separator = ctx.config.read(key=ctx.current_blog + ':meta_format')
    if meta_separator:
        meta_signs = [i.strip() for i in meta_separator.strip().split(" ")]
        try:
            meta_start, meta_end = meta_signs
        except:
            raise SystemExit("Invalid custom meta format", meta_signs)

    else:
        meta_start, meta_end = '<!--', '-->'

    ipynb_dict = json.loads(ipynb_data)

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

        meta = [i for i in meta_list[first_mark+1:second_mark]]
        metadata = dict()
        for key_value in meta:
            key, value = key_value.split(':')
            if value:
                metadata[key.strip()] = value.strip()

        del ipynb_dict['cells'][0]
        main_data = json.dumps(ipynb_dict)
        return main_data, metadata

    except Exception as E:
        ctx.log("Ipynb file is empty")
        return ipynb_data, metadata


    html_exporter = gen_exporter()
    meta = dict()
    nb = nbformat.reads(ipynb_content, as_version=4)
    (body, __) = html_exporter.from_notebook_node(nb)
    return meta, body


def gen_exporter():
    c = TraitletsConfig()
    c.htmlexporter.preprocessors = [
        'nbconvert.preprocessors.extractoutputpreprocessor']
    # create the new exporter using the custom config
    html_exporter = HTMLExporter(config=c)
    html_exporter.template_file = 'basic'
    return html_exporter
