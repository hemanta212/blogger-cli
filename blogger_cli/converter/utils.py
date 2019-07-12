import os
from collections import OrderedDict


def extract_main_and_meta_from_file_content(ctx, file_data):
    meta = OrderedDict()
    meta_start, meta_end = extract_meta_format(ctx)
    first_mark = file_data.find(meta_start) + len(meta_start)
    second_mark = file_data.find(meta_end)
    if not -1 in (first_mark, second_mark):
        metadata = file_data[first_mark: second_mark]
        metadata = os.linesep.join([s for s in metadata.splitlines() if s])

    main_data = file_data[second_mark + len(meta_end): ]
    meta_lines = metadata.strip().split('\n')

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
