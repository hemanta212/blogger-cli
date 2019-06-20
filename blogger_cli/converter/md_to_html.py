import os
from shutil import copyfile, SameFileError
from urllib.request import urlopen, Request

import markdown
from bs4 import BeautifulSoup as BS

from blogger_cli.converter.extractors import extract_and_write_images


def convert_and_copy_to_blog(ctx, md_file):
    md_file_path = os.path.abspath(os.path.expanduser(md_file))
    meta, html_body = convert(md_file_path)
    html_filename_meta = write_html_and_md(ctx, html_body,
                                            md_file_path, meta)
    return html_filename_meta


def convert(md_file_path):
    with open(md_file_path, 'r', encoding='utf8') as rf:
        md_data = rf.read()

    meta, main_md = extract_meta_and_main(md_data)
    extensions = ['extra', 'smarty']
    html = markdown.markdown(main_md, extensions=extensions,
                            output_format='html5')
    return meta, html


def extract_meta_and_main(md_data):
    metadata = ''
    first_mark = md_data.find('<!--') + 4
    second_mark = md_data.find('-->')
    if not -1 in (first_mark, second_mark):
        metadata = md_data[first_mark: second_mark]

    main_data = md_data[second_mark+4:]
    meta_lines = metadata.strip().split('\n')
    meta = dict()

    try:
        for key_value in meta_lines:
            key, value = key_value.split(':')
            meta[key.strip()] = value.strip()
    except:
        main_data = md_data

    return meta, main_data


def write_html_and_md(ctx, html_body, md_file_path, meta):
    md_filename = os.path.basename(md_file_path)
    destination_dir = ctx.conversion['destination_dir']
    override_meta = ctx.conversion['override_meta']

    given_topic = ctx.conversion.get('topic')
    meta_topic = meta.get('topic') if meta else None
    topics = (meta_topic, given_topic)
    available_topic = [topic for topic in topics if topic]

    if len(available_topic) == 2:
        topic = given_topic if override_meta else meta_topic
    elif available_topic:
        topic = available_topic[0]
    else:
        topic = ''

    ctx.log(":: Got topic, ", topic)
    md_filename = os.path.join(topic, md_filename)
    html_filename = md_filename.replace('.md', '.html')
    html_file_path = os.path.join(destination_dir, html_filename)
    new_md_file_path = os.path.join(destination_dir, md_filename)
    new_blog_post_dir = os.path.dirname(html_file_path)
    ctx.vlog("New blog_posts_dir finalized::", new_blog_post_dir)

    if not os.path.exists(new_blog_post_dir):
        os.mkdir(new_blog_post_dir)

    extract_img = ctx.conversion['extract_img']
    if extract_img:
        html_body = extract_and_write_images(ctx, html_body,
                                            md_filename, new_blog_post_dir)

    with open(html_file_path, 'w', encoding='utf8') as wf:
        wf.write(html_body)
        ctx.log(":: Converted basic html to", html_file_path)

    try:
        copyfile(md_file_path, new_md_file_path)
        ctx.log(":: Copied md file to", new_md_file_path, '\n')
    except  SameFileError:
        os.remove(new_md_file_path)
        copyfile(md_file_path, new_md_file_path)
        ctx.log(":: Overwriting md file", new_md_file_path, '\n')

    return (html_filename, meta)

