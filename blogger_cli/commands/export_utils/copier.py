import os
import json
from distutils.dir_util import copy_tree
from distutils.file_util import copy_file
from pkg_resources import resource_filename, resource_string

import jinja2
from blogger_cli import RESOURCE_DIR
from blogger_cli.blog_manager.add_post import get_snippet_content_map


def copy_design_assets(ctx, export_path):
    design_asset_path = os.path.join(RESOURCE_DIR, 'blog_layout', 'assets')
    ctx.vlog("Copying design assets from", design_asset_path,
            os.listdir(design_asset_path))
    copy_tree(design_asset_path, export_path)
    return design_asset_path


def copy_blog_template(ctx, export_path):
    blog_template_dir = os.path.join(RESOURCE_DIR, 'blog_layout',
                                    '_blogger_templates')
    build_indexes(ctx)
    ctx.vlog("Copying blog template from", blog_template_dir,
            os.listdir(blog_template_dir))
    copy_tree(blog_template_dir, export_path)
    return blog_template_dir


def copy_blog_layout(ctx, export_path):
    blog_layout_dir = os.path.join(RESOURCE_DIR, 'blog_layout')
    build_indexes(ctx)
    ctx.vlog("Copying blog template from", blog_layout_dir,
            os.listdir(blog_layout_dir))
    copy_tree(blog_layout_dir, export_path)
    images_folder = os.path.join(export_path, 'images')
    if not os.path.exists(images_folder):
        os.mkdir(images_folder)
    return blog_layout_dir


def build_indexes(ctx):
    blog = ctx.current_blog
    templates_dir = ctx.config.read(key=blog+':templates_dir')
    if templates_dir:
        templates_dir = os.path.normpath(os.path.expanduser(templates_dir))

    ctx.conversion = {
            'templates_dir' : templates_dir
    }
    meta = dict()
    snippet = get_snippet_content_map(ctx, meta)
    indexes = ['main_index.html', 'blog_index.html']
    index_template_paths = ['resources/' + index for index in indexes]
    dest_index_paths = {
            'main_index.html': 'resources/blog_layout/index.html',
            'blog_index.html': 'resources/blog_layout/blog/index.html',
    }

    for index_path in index_template_paths:
        index_layout = resource_string('blogger_cli', index_path).decode('utf-8')
        index_template = jinja2.Template(index_layout).render(snippet=snippet)
        index_filename = os.path.basename(index_path)
        dest_index_filename = resource_filename('blogger_cli',
                            dest_index_paths[index_filename])
        with open(dest_index_filename, 'w') as wf:
            wf.write(index_template)


def copy_blog_config(ctx, export_dir):
    blog = ctx.current_blog
    blog_config = ctx.config.read(key=blog)
    export_path = os.path.join(export_dir, blog+'.json')
    ctx.vlog("Copying blog config for", blog, "to", export_path)
    with open(export_path, 'w') as wf:
        json.dump(blog_config, wf, indent=2)
    return blog_config


def copy_blog_index(ctx, export_path):
    build_indexes(ctx)
    blog_index_path = resource_filename('blogger_cli',
            'resources/blog_layout/blog/index.html')
    ctx.vlog("Copying blog index from", blog_index_path)
    copy_file(blog_index_path, export_path)
    return blog_index_path

