#!/usr/bin/env python
import os
from shutil import copyfile, SameFileError
from urllib.request import urlopen, Request

import markdown
from bs4 import BeautifulSoup as BS


def convert_and_copy_to_blog(ctx, md_file):
    md_file_path = os.path.abspath(os.path.expanduser(md_file))
    html_body = convert(md_file_path)
    html_filename = write_html_and_md(ctx, html_body,
                                    md_file_path)
    return html_filename


def convert(md_file_path):
    with open(md_file_path, 'r', encoding='utf8') as rf:
        md = rf.read()

    extensions = ['extra', 'smarty']
    html = markdown.markdown(md, extensions=extensions, output_format='html5')
    return html


def write_html_and_md(ctx, html_body, md_file_path):
    destination_dir = ctx.conversion['destination_dir']
    extract_img = ctx.conversion['extract_img']
    md_filename = os.path.basename(md_file_path)
    html_filename = md_filename.replace('.md', '.html')
    html_file_path = os.path.join(destination_dir, html_filename)
    new_md_file_path = os.path.join(destination_dir, md_filename)
    if extract_img:
        html_body = get_image_extracted_html(ctx, html_file_path, html_body)

    with open(html_file_path, 'w', encoding='utf8') as wf:
        wf.write(html_body)
        print("File written", html_file_path)

    try:
        copyfile(md_file_path, new_md_file_path)
    except  SameFileError:
        pass

    return html_filename


def get_image_extracted_html(ctx, html_file_path, html_body):
    img_dir = ctx.conversion['img_dir']
    html_filename = os.path.basename(html_file_path)
    image_dirname = os.path.splitext(html_filename)[0]
    image_dir_path = os.path.join(img_dir, image_dirname)

    ctx.vlog("Extracting images: img folder", image_dir_path)
    if not os.path.exists(image_dir_path):
        os.makedirs(image_dir_path)

    html_body = extract_and_write_images(ctx, html_body, image_dir_path)
    return html_body


def extract_and_write_images(ctx, html_body, image_dir_path):
    soup = BS(html_body, 'html.parser')
    images = soup.find_all('img')
    destination_dir = ctx.conversion['destination_dir']
    ctx.vlog("Found", len(images), "images")

    for index, img_tag in enumerate(images):
        img_data = img_tag['src']
        image_name = 'image_' + str(index+1) + '.png'
        image_path = os.path.join(image_dir_path, image_name)

        if img_data.startswith('http'):
            ctx.vlog("Image from url detected. Trying to download", img_data)
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh;Intel ' +
                    'Mac OS X 10_10_1) AppleWebKit/537.36(KHTML, like Gecko)'+
                    ' Chrome/39.0.2171.95 Safari/537.36'}

            try:
                req = Request(img_data, headers=headers)
                with urlopen(req) as response:
                    raw_image = response.read()

                with open(image_path, 'wb') as wf:
                    wf.write(raw_image)

                image_src = get_image_src(destination_dir, image_path)
                img_tag['src'] = image_src
                ctx.vlog("Replacing source tag with:", image_src)

            except Exception as E:
                ctx.vlog(E, "skipping  the image.")
                pass

    return soup.decode('utf8')

def get_image_src(destination_dir, image_path):
    os.chdir(destination_dir)
    src_path = os.path.relpath(image_path)
    return src_path

