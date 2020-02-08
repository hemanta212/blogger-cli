import os
import shutil
from datetime import datetime
from pathlib import Path

import click

from blogger_cli.blog_manager import add_post
from blogger_cli.cli import pass_context
from blogger_cli.commands.convert_utils.classifier import convert_and_copyfiles


@click.command("convert", short_help="Convert files to html")
@click.argument(
    "path", nargs=-1, required=False, type=click.Path(exists=True, readable=True)
)
@click.option(
    "--recursive",
    "-r",
    "recursive",
    is_flag=True,
    help="Recusively search folder for files to convert. USE WITH CAUTION",
)
@click.option(
    "--not-code",
    "iscode",
    is_flag=True,
    default=True,
    help="Do not add mathjax and code support",
)
@click.option(
    "-o",
    "destination_dir",
    type=click.Path(exists=True, writable=True),
    help="Destination for converted files,DEFAULT from blog_config",
)
@click.option("-b", "--blog", help="Name of the blog")
@click.option(
    "-ex-html",
    "--exclude-html",
    "exclude_html",
    is_flag=True,
    help="Ignore html files from conversion",
)
@click.option(
    "--img-dir",
    "img_dir",
    type=click.Path(exists=True),
    help="Folder for post images. Default: blog's config, Destination dir",
)
@click.option(
    "-no-ex",
    "--no-extract",
    "extract_static",
    is_flag=True,
    default=True,
    help="Disable resource extraction from files like images from ipynbs",
)
@click.option(
    "-t",
    "--topic",
    "topic",
    type=str,
    help="Topic in which this post should be placed in index",
)
@click.option(
    "-temp",
    "--template",
    "templates_dir",
    type=click.Path(exists=True),
    help="Folder path of custom templates",
)
@click.option(
    "--override-meta",
    "override_meta",
    is_flag=True,
    help="Ignore meta topic in favour of --topic option",
)
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose flag")
@pass_context
def cli(
    ctx,
    path,
    iscode,
    blog,
    exclude_html,
    extract_static,
    destination_dir,
    img_dir,
    topic,
    templates_dir,
    recursive,
    override_meta,
    verbose,
):
    """
    Convert from diffrent file format to html

   Usage:\n
    blogger convert filename.ipynb\n
    blogger convert file1 file2 file3 -b blog1 -no-imgex\n
    blogger convert file1 file2 file3 -b blog1 --topic Tech\n
    blogger convert filename --not-code -o ~/username.github.io

    blogger convert ../folder1 file1 ../folder2  -v \n
    blogger convert -r ../folder1 file1 ../folder2  -v \n
    blogger convert  ../folder1 file1 ../folder2  --exclude-html -v
    """
    ctx.verbose = verbose
    set_current_blog(ctx, blog)
    path = path if path else get_files_from_working_dir(ctx, recursive)
    if not path:
        ctx.log(":: All files synced.")
        raise SystemExit(0)

    resolved_files = get_files_being_converted(path, recursive=recursive)
    file_ext_map = get_file_ext_map(ctx, exclude_html, resolved_files)
    destination_dir = check_and_ensure_destination_dir(ctx, destination_dir)
    img_dir = check_and_ensure_img_dir(ctx, destination_dir, img_dir)
    templates_dir = resolve_templates_dir(ctx, templates_dir)

    ctx.log("\nCONVERTING", len(file_ext_map), "FILES")
    ctx.vlog(
        "Got files and ext:",
        file_ext_map,
        "img_dir:",
        img_dir,
        "templates_dir:",
        templates_dir,
    )

    ctx.conversion = {
        "file_ext_map": file_ext_map,
        "destination_dir": destination_dir,
        "iscode": iscode,
        "img_dir": img_dir,
        "extract_static": extract_static,
        "templates_dir": templates_dir,
        "override_meta": override_meta,
        "topic": topic,
    }
    filenames_meta = convert_and_copyfiles(ctx)
    ctx.log("Converted files successfully. \n")
    ctx.log("ADDING FILES TO BLOG")
    for filename_meta in filenames_meta:
        add_post.add(ctx, filename_meta)


def get_files_from_working_dir(ctx, recursive):
    ctx.log("\n:: No input files given. Scanning working folder for changes..")
    blog = ctx.current_blog
    last_checked = ctx.config.read(key=blog + ": working_dir_timestamp")
    working_dir = ctx.config.read(key=blog + ": working_dir")
    working_dir = Path(str(working_dir))
    if not working_dir or not working_dir.exists():
        ctx.log(":: Working folder doesnot exist")
        ctx.log(":: ERROR: No input files")
        raise SystemExit()

    current_timestamp = datetime.today().timestamp()
    ctx.config.write(blog + ":working_dir_timestamp", current_timestamp)

    if not last_checked:
        return str(working_dir)

    try:
        last_checked = float(last_checked)
    except:
        ctx.log(
            "Parse error for last sync. Please convert",
            "files manually or convert all files in your working_dir",
            "ERROR: Last sync date invalid",
        )
        raise SystemExit()

    def is_modified_file(path):
        if not path.is_file():
            return False
        if path.lstat().st_mtime >= last_checked:
            return True

        return False

    all_files = []

    for item in working_dir.iterdir():
        if item.is_file():
            if is_modified_file(item):
                all_files.append(str(item.resolve()))
            else:
                continue

        elif recursive:
            items = item.rglob("*")
            files = [str(i.resolve()) for i in items if is_modified_file(i)]
            all_files += files

    return all_files


def get_files_being_converted(path, recursive=False):
    isfolder = lambda x: True if os.path.isdir(x) else False
    all_files = []
    for item in path:
        if not isfolder(item):
            abs_file_path = os.path.abspath(item)
            all_files.append(abs_file_path)
            continue

        if recursive:
            items = Path(item).rglob("*")
            files = [str(i.resolve()) for i in items if i.is_file()]
            all_files += files
        elif not recursive:
            items = get_all_files(item)
            all_files += items

    return set(all_files)


def get_all_files(folder):
    files = []
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        if os.path.isfile(file_path):
            abs_file_path = os.path.abspath(file_path)
            files.append(abs_file_path)
    return files


def check_and_ensure_destination_dir(ctx, output_dir):
    blog = ctx.current_blog
    blog_dir = ctx.config.read(key=blog + ": blog_dir")
    posts_dir = ctx.config.read(key=blog + " : blog_posts_dir")
    if not posts_dir and not output_dir:
        ctx.log(
            "No target folder set. Specify one with -o option or",
            "setup in your",
            blog,
            "blog's config",
            "ERROR: NO OUTPUT FOLDER",
        )
        raise SystemExit()

    if posts_dir:
        destination_dir = os.path.join(blog_dir, posts_dir)

    if output_dir:
        destination_dir = output_dir

    destination_dir = os.path.normpath(os.path.expanduser(destination_dir))
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    return destination_dir


def check_and_ensure_img_dir(ctx, destination_dir, output_img_dir):
    blog = ctx.current_blog
    blog_dir = ctx.config.read(key=blog + ": blog_dir")
    blog_img_dir = ctx.config.read(key=blog + ": blog_images_dir")

    if not blog_img_dir and not output_img_dir:
        ctx.log(
            "No images folder given. Specify one with -o option or",
            "setup in your",
            blog,
            "blog's config",
        )
        ctx.log("If you want to avoid extracting images use -no-ex  option.")

        if click.confirm("Put images dir in same folder as blog posts?"):
            img_dir = os.path.join(destination_dir, "images")
            return img_dir
        else:
            ctx.log("ERROR: NO OUTPUT FOLDER")
            raise SystemExit()

    if blog_img_dir:
        img_dir = os.path.join(blog_dir, blog_img_dir)

    if output_img_dir:
        img_dir = output_img_dir

    img_dir = os.path.normpath(os.path.expanduser(img_dir))
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    return img_dir


def resolve_templates_dir(ctx, templates_dir_from_cmd):
    blog = ctx.current_blog
    blog_templates_dir = ctx.config.read(key=blog + ": templates_dir")
    templates_dir = blog_templates_dir

    if templates_dir_from_cmd:
        templates_dir = templates_dir_from_cmd

    if templates_dir:
        templates_dir = os.path.normpath(os.path.expanduser(templates_dir))
    return templates_dir


def set_current_blog(ctx, blog):
    current_blog = ctx.default_blog
    if blog:
        current_blog = blog

    if not ctx.blog_exists(current_blog):
        ctx.log("Blog name not given. Use --blog option or set default blog")
        ctx.log("ERROR: Blogname unavailable. SEE blogger convert --help")
        raise SystemExit()

    ctx.current_blog = current_blog


def get_file_ext_map(ctx, exclude_html, files_being_converted):
    file_ext_map = {}

    if exclude_html:
        ctx.SUPPORTED_EXTENSIONS.remove("html")

    for file in files_being_converted:
        ext = get_file_ext(file)
        if ext in ctx.SUPPORTED_EXTENSIONS:
            file_ext_map[file] = ext
        else:
            ctx.log("Unsupported ext", ext, "Skipping")
            continue

    return file_ext_map


def get_file_ext(file):
    extension = os.path.splitext(file)[1]
    return extension[1:]
