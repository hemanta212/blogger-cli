import os.path
from shutil import copyfile

from blogger_cli.converter import ipynb_to_html, md_to_html


def convert_and_copyfiles(ctx):
    file_ext_map = ctx.conversion["file_ext_map"]
    filenames_meta = []

    convert_file = {
        "md": md_to_html.convert_and_copy_to_blog,
        "ipynb": ipynb_to_html.convert_and_copy_to_blog,
        "html": process_htmlfile,
        "htm": process_htmlfile,
    }

    for file, filetype in file_ext_map.items():
        ctx.log("\n:: Processing the file", file, "filetype:", filetype)
        converter = convert_file[filetype]
        html_filename_meta = converter(ctx, file)
        filenames_meta.append(html_filename_meta)

    return filenames_meta


def process_htmlfile(ctx, html_file):
    destination_dir = ctx.conversion["destination_dir"]
    html_filename = os.path.basename(html_file)

    given_topic = ctx.conversion.get("topic")
    topic = given_topic if given_topic else ""
    if topic:
        ctx.log(":: Got topic, ", topic)

    html_filename = os.path.join(topic, html_filename)
    html_file_path = os.path.join(destination_dir, html_filename)
    meta = {"_summary_": ""}
    ctx.log(":: Copying basic html file to", html_file_path)

    if html_file != html_file_path:
        try:
            copyfile(html_file, html_file_path)
        except Exception as E:
            os.remove(html_file_path)
            copyfile(html_file, html_file_path)
            ctx.log(":: ERROR", E, "Overwriting html file", html_file_path)

    return (html_filename, meta)
