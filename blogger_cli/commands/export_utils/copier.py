import os
import json
from distutils.dir_util import copy_tree
from distutils.file_util import copy_file
from pkg_resources import resource_filename

from blogger_cli import resource_dir


def copy_design_assets(ctx, export_path):
    design_asset_path = os.path.join(resource_dir, 'blog_template', 'assets')
    copy_tree(design_asset_path, export_path)


def copy_blog_template(ctx, export_path):
    blog_template_dir = os.path.join(resource_dir, 'blog_template')
    copy_tree(blog_template_dir, export_path)


def copy_blog_config(ctx, export_dir):
    blog = ctx.current_blog
    blog_config = ctx.config.read(key=blog)
    export_path = os.path.join(export_dir, blog+'.json')
    blog_config = json.dumps(blog_config, indent=2)
    with open(export_path, 'w') as wf:
        json.dump(blog_config, wf, indent=2)


def copy_blog_index(ctx, export_path):
    blog_index_path = resource_filename('blogger_cli',
            'resources/blog_template/blog/index.html')
    copy_file(blog_index_path, export_path)

