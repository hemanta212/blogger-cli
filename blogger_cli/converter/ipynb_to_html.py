import os
from shutil import copyfile, SameFileError
from base64 import b64decode
from urllib.request import urlopen, Request

from bs4 import BeautifulSoup as BS
from nbconvert import HTMLExporter
import nbformat
from traitlets.config import Config as TraitletsConfig


def convert_and_copy_to_blog(ctx, ipynb_file):
    ipynb_file_path = os.path.abspath(os.path.expanduser(ipynb_file))
    ctx.vlog("Got file", ipynb_file_path, "Converting to basic html body")
    html_body = convert(ipynb_file_path)
    html_filename  = write_html_and_ipynb(ctx, ipynb_file_path, html_body)
    return html_filename


def write_html_and_ipynb(ctx, ipynb_file_path, html_body):
    extract_img = ctx.conversion['extract_img']
    destination_dir = ctx.conversion['destination_dir']
    ipynb_filename = os.path.basename(ipynb_file_path)
    html_filename = ipynb_filename.replace('.ipynb', '.html')
    html_file_path = os.path.join(destination_dir, html_filename)
    new_ipynb_file_path = os.path.join(destination_dir, ipynb_filename)

    if extract_img:
        html_body = get_image_extracted_html(ctx, html_file_path, html_body)
    ctx.vlog("Writing html body to file", html_file_path)

    with open(html_file_path, 'w', encoding='utf8') as wf:
        wf.write(html_body)
    try:
        copyfile(ipynb_file_path, new_ipynb_file_path)
    except SameFileError:
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

    if  not os.listdir(image_dir_path):
        os.rmdir(image_dir_path)

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

        if img_data.startswith('data:image/png;base64,'):
            __, encoded = img_data.split(",", 1)
            data = b64decode(encoded)
            ctx.vlog("Writing ", index+1, "data uri to image:", image_path)
            with open(image_path, 'wb') as wf:
                wf.write(data)

            image_src = get_image_src(destination_dir, image_path)
            img_tag['src'] = image_src
            ctx.vlog("Replacing source tag with:", image_src)


        elif img_data.startswith('http'):
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


def convert(ipynb_file):
    with open(ipynb_file, 'r', encoding='utf8') as rf:
        ipynb_content = rf.read()

    html_exporter = gen_exporter()
    nb = nbformat.reads(ipynb_content, as_version=4)
    (body, __) = html_exporter.from_notebook_node(nb)
    return body


def gen_exporter():
    c = TraitletsConfig()
    c.htmlexporter.preprocessors = [
        'nbconvert.preprocessors.extractoutputpreprocessor']
    # create the new exporter using the custom config
    html_exporter = HTMLExporter(config=c)
    html_exporter.template_file = 'basic'
    return html_exporter

