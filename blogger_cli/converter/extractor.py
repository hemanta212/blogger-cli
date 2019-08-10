import os
import shutil
from base64 import b64decode
from pathlib import Path
from collections import OrderedDict

from bs4 import BeautifulSoup as BS
from urllib.request import Request, urlopen


def extract_and_write_static(ctx, html_body, blog_post_dir, topic_filename):
    global EXTRACT_LIST
    blog = ctx.current_blog
    EXTRACT_LIST = ctx.config.read(key=blog+':post_extract_list')
    if not EXTRACT_LIST:
        EXTRACT_LIST = ['URI', 'URL']

    static_dir = ctx.conversion['img_dir']

    topic = os.path.dirname(topic_filename)
    filename = os.path.basename(topic_filename)
    name, ext = os.path.splitext(filename)
    static_path = os.path.join(static_dir, topic, name)
    if not os.path.exists(static_path):
        os.makedirs(static_path)

    soup = BS(html_body, 'html.parser')
    images = soup.find_all('img')
    ctx.log(":: Found", len(images), "images")
    extract_images(ctx, images, static_path, filename, blog_post_dir)

    videos = soup.find_all('video')
    extract_videos(ctx, videos, static_path, filename, blog_post_dir)
    ctx.log(":: Found", len(videos), "videos")

    if not os.listdir(static_path):
        os.rmdir(static_path)

    return soup.decode('utf8')


def extract_videos(ctx, videos, video_path, filename, blog_post_dir):
    def get_name_from_title(video_tag):
        try:
            video_name = video_tag['title'].strip().lower()
        except:
            video_name = None
        return video_name


    def get_video_data(video_tag):
        try:
            video_data = video_tag['src']
        except:
            video_data = video_tag.source['src']
        return video_data



    for index, video_tag in enumerate(videos):
        try:
            video_data = get_video_data(video_tag)
        except:
            ctx.log("Cannot find src attribute. Skipping...")
            continue

        video_name = get_name_from_title(video_tag)

        if not video_name:
            video_name = 'video_' + str(index+1)

        video_name = video_name.replace(' ', '_').replace('.','_') + '.mp4'
        video_path = os.path.join(video_path, video_name)

        if (video_data.startswith('data:video/mp4;base64,')
            and 'URI' in EXTRACT_LIST):

            ctx.log(":: Detected DATA URI video. Writing to", video_path)
            video_tag = extract_and_write_uri(video_data, video_tag, video_path,
                                        blog_post_dir)
        else:
            file_path = get_absolute_path(ctx, filename)
            dest_path = os.path.dirname(video_path)
            extracted_path = extract_static_files(ctx, video_data,
                                                  file_path, dest_path)
            if extracted_path:
                ctx.log(":: Detected STATIC video. Copying to", extracted_path)
                new_video_src = get_static_src(blog_post_dir, extracted_path)
                video_tag['src'] = new_video_src


def extract_images(ctx, images, img_path, filename, blog_post_dir):
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

        if (img_data.startswith('data:image/png;base64,')
            and 'URI' in EXTRACT_LIST):

            ctx.log(":: Detected DATA URI img. Writing to", image_path)
            img_tag = extract_and_write_uri(img_data, img_tag, image_path,
                                        blog_post_dir)
        elif ( (img_data.startswith('http') or img_data.startswith('https'))
                and 'URL' in EXTRACT_LIST):
            img_tag = extract_and_write_url_img(ctx, img_data, img_tag,
                                                image_path, blog_post_dir)
        else:
            file_path = get_absolute_path(ctx, filename)
            dest_path = os.path.dirname(image_path)
            extracted_path = extract_static_files(ctx, img_data,
                                                  file_path, dest_path)
            if extracted_path:
                ctx.log(":: Detected STATIC img. Copying to", extracted_path)
                new_img_src = get_static_src(blog_post_dir, extracted_path)
                img_tag['src'] = new_img_src


def extract_and_write_uri(data, tag, static_path, blog_post_dir):
    __, encoded = data.split(",", 1)
    data = b64decode(encoded)
    with open(static_path, 'wb') as wf:
        wf.write(data)

    static_src = get_static_src(blog_post_dir, static_path)
    tag['src'] = static_src
    return tag


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

        image_src = get_static_src(blog_post_dir, image_path)
        img_tag['src'] = image_src
        ctx.vlog(":: Replacing source tag with:", image_src)
    except Exception as E:
        ctx.vlog(":: skipping  the image.", E)
        pass

    return img_tag


def get_static_src(destination_dir, static_path):
    os.chdir(destination_dir)
    src_path = os.path.relpath(static_path)
    return src_path


def get_absolute_path(ctx, filename):
    all_files = ctx.conversion['file_ext_map'].keys()

    file_path = [file for file in all_files if filename in file]
    return file_path[0]


def extract_static_files(ctx, file_name, file_path, dest_dir):
    '''
    This function will look for static local files that were linked
    from inside ipynb file. The path is built dynamically according
    to the one provided in ipynb file.

    Eg: ('learning.mp4')
    The learning.mp4 file will be searched in same dir as of original
    ipynb file.

    Eg: ('../learning.mp4)
    Similarly, now blogger will look learning.mp4 in the parent dir of
    original ipynb file.

    NOTE: In cases where the ipynb file was previously converted and is
    located  inside the blog_dir then entire blog_dir will be searched
    for that image and the path that contain topic/ipynb_filename will
    be selected as static_path. What this means if You have to use same
    topic as before to make use of this.
    '''

    orig_dir = Path(os.path.dirname(file_path))
    static_path = orig_dir / file_name
    file_name = os.path.basename(file_name)  # manage cases like ../../video.mp4

    # Detect if the original file is in blog dir itself
    blog_dir = Path(ctx.config.read(key=ctx.current_blog + ':blog_dir'))
    blog_dir = blog_dir.expanduser()

    is_inside_blog_dir = False
    if str(blog_dir) in file_path:
        is_inside_blog_dir = True

    # Provide the static files path if orig file is in blog_dir
    if not static_path.exists() and is_inside_blog_dir:
        dest_dir_parts = Path(dest_dir).parts
        topic_filename = Path(dest_dir_parts[-2]) / dest_dir_parts[-1]

        image_dirs = list(blog_dir.rglob(str(topic_filename)))

        while not static_path.exists() and image_dirs:
            static_path_dir = image_dirs.pop(0)
            static_path = static_path_dir / file_name

    if static_path.exists():
        static_path = static_path.resolve()
        dest_path = os.path.join(dest_dir, file_name)
        try:
            shutil.copyfile(str(static_path), dest_path)
        except shutil.SameFileError:
            pass

        return dest_path



def extract_main_and_meta_from_file_content(ctx, file_data):
    metadata = ''
    meta_start, meta_end = extract_meta_format(ctx)
    first_mark = file_data.find(meta_start) + len(meta_start)
    second_mark = file_data.find(meta_end)
    if not -1 in (first_mark, second_mark):
        metadata = file_data[first_mark: second_mark]
        metadata = os.linesep.join([s for s in metadata.splitlines() if s])

    main_data = file_data[second_mark + len(meta_end): ]
    meta_lines = metadata.strip().split('\n')

    meta = OrderedDict()
    try:
        for key_value in meta_lines:
            key, value = key_value.split(':')
            meta[key.strip()] = value.strip()
    except:
        main_data = file_data

    ctx.vlog(":: Got metadata", meta)
    return main_data, meta


def extract_meta_format(ctx):
    meta_separator = ctx.config.read(key=ctx.current_blog + ':meta_format')
    if meta_separator:
        meta_signs = [i.strip() for i in meta_separator.strip().split(" ")]
        try:
            meta_start, meta_end = meta_signs
        except:
            raise SystemExit("Invalid custom meta format", meta_signs)

    else:
        meta_start, meta_end = '<!--', '-->'

    return meta_start, meta_end


def replace_ext(file_path, ext):
    file_dir = os.path.dirname(file_path)
    orig_filename_ext = os.path.basename(file_path)
    orig_filename = os.path.splitext(orig_filename_ext)[0]
    new_filename = orig_filename + ext
    new_file_path = os.path.join(file_dir, new_filename)
    return new_file_path


def extract_topic(ctx, meta):
    override_meta = ctx.conversion.get('override_meta')
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

    return topic
