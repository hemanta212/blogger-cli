import os
from base64 import b64decode

from bs4 import BeautifulSoup as BS
from urllib.request import Request, urlopen



def extract_and_write_images(ctx, html_body, topic_filename, blog_post_dir):
    img_dir = ctx.conversion['img_dir']
    topic = os.path.dirname(topic_filename)
    filename = os.path.basename(topic_filename)
    name, ext = os.path.splitext(filename)
    img_path = os.path.join(img_dir, topic, name)
    if not os.path.exists(img_path):
        os.makedirs(img_path)

    soup = BS(html_body, 'html.parser')
    images = soup.find_all('img')
    ctx.log(":: Found", len(images), "images")

    for index, img_tag in enumerate(images):
        img_data = img_tag['src']
        try:
            image_name = img_tag['title'].strip().lower()
        except:
            image_name = None

        if not image_name:
            image_name = 'image_' + str(index+1)

        image_name = image_name.replace(' ','_').replace('.','_') + '.png'
        image_path = os.path.join(img_path, image_name)

        if img_data.startswith('data:image/png;base64,'):
            ctx.log(":: Detected DATA URI img. Writing to", image_path)
            img_tag = extract_and_write_uri_img(img_data, img_tag, image_path,
                                        blog_post_dir)
        elif img_data.startswith('http'):
            img_tag = extract_and_write_url_img(ctx, img_data, img_tag,
                                                image_path, blog_post_dir)

    if not os.listdir(img_path):
        os.rmdir(img_path)

    return soup.decode('utf8')


def extract_and_write_uri_img(img_data, img_tag, image_path, blog_post_dir):
    __, encoded = img_data.split(",", 1)
    data = b64decode(encoded)
    with open(image_path, 'wb') as wf:
        wf.write(data)

    image_src = get_image_src(blog_post_dir, image_path)
    img_tag['src'] = image_src
    return img_tag


def extract_and_write_url_img(ctx, img_data, img_tag,
                            image_path, blog_post_dir):
    ctx.vlog(":: Downloading image from", img_data)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh;Intel ' +
            'Mac OS X 10_10_1) AppleWebKit/537.36(KHTML, like Gecko)'+
            ' Chrome/39.0.2171.95 Safari/537.36'}
    try:
        req = Request(img_data, headers=headers)
        with urlopen(req) as response:
            raw_image = response.read()

        ctx.log(":: Detected url image. Writing to", image_path)
        with open(image_path, 'wb') as wf:
            wf.write(raw_image)

        image_src = get_image_src(blog_post_dir, image_path)
        img_tag['src'] = image_src
        ctx.vlog("Replacing source tag with:", image_src)
    except Exception as E:
        ctx.vlog("skipping  the image.", E)
        pass

    return img_tag


def get_image_src(destination_dir, image_path):
    os.chdir(destination_dir)
    src_path = os.path.relpath(image_path)
    return src_path

