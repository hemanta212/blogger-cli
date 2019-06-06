import os
import json
from distutils.dir_util import copy_tree
from distutils.file_util import copy_file
from pkg_resources import resource_filename

from blogger_cli import resource_dir


def copy_design_assets(ctx, export_path):
    design_asset_path = os.path.join(resource_dir, 'blog_template', 'assets')
    ctx.vlog("Copying design assets from", design_asset_path,
            os.listdir(design_asset_path))
    copy_tree(design_asset_path, export_path)


def copy_blog_template(ctx, export_path):
    blog_template_dir = os.path.join(resource_dir, 'blog_template')
    ctx.vlog("Copying blog template from", blog_template_dir,
            os.listdir(blog_template_dir))
    copy_tree(blog_template_dir, export_path)
    images_folder = os.path.join(export_path, 'images')
    if not os.path.exists(images_folder):
        os.mkdir(images_folder)


def copy_blog_config(ctx, export_dir):
    blog = ctx.current_blog
    blog_config = ctx.config.read(key=blog)
    export_path = os.path.join(export_dir, blog+'.json')
    blog_config = json.dumps(blog_config, indent=2)
    ctx.vlog("Copying blog config for", blog, "to", export_path)
    with open(export_path, 'w') as wf:
        json.dump(blog_config, wf, indent=2)


def copy_blog_index(ctx, export_path):
    blog_index_path = resource_filename('blogger_cli',
            'resources/blog_template/blog/index.html')
    ctx.vlog("Copying blog index from", blog_index_path)
    copy_file(blog_index_path, export_path)

