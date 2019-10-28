import os

import click

from blogger_cli import CONFIG_DIR
from blogger_cli.cli_utils.json_writer import Config


def save_post_meta(ctx, snippet, meta):
    config = get_config(ctx)
    topic_filename = snippet["link"]
    blog_topic_filename = os.path.join(ctx.current_blog, topic_filename)
    summary = meta["_summary_"]
    title = snippet["title"]
    postmeta = {"title": title, "content": summary}
    config.write(blog_topic_filename, postmeta)


def get_blog_posts_dir(ctx):
    blog = ctx.current_blog
    blog_posts_dir = ctx.config.read(blog + ":blog_posts_dir")
    if not blog_posts_dir:
        ctx.log(":: Failed to build file link! no proper blog dir")
        blog_posts_dir = ""
    return blog_posts_dir


def get_topic_filename(ctx, file_path):
    blog = ctx.current_blog
    blog_posts_dir = ctx.config.read(key=blog + ": blog_posts_dir")
    blog_dir = ctx.config.read(key=blog + ":blog_dir")
    blog_posts_path = os.path.join(blog_dir, blog_posts_dir)
    topic_filename = os.path.relpath(file_path, blog_posts_path)
    return topic_filename


def get_post_meta(ctx, file_path, post_meta):
    config = get_config(ctx)
    topic_filename = get_topic_filename(ctx, file_path)
    posts_dir = get_blog_posts_dir(ctx)
    post_meta["link"] = os.path.join(posts_dir, topic_filename)

    blog_topic_filename = os.path.join(ctx.current_blog, topic_filename)
    cached_post_meta = config.read(key=blog_topic_filename)
    default_post_meta = post_meta.copy()

    for key, value in default_post_meta.items():
        cached_value = None
        if cached_post_meta:
            cached_value = cached_post_meta.get(key)

        if not value and cached_value:
            post_meta[key] = cached_value
        elif not value and not cached_value:
            del post_meta[key]

    if not post_meta:
        click.secho(
            (
                ":: ERROR: Metadata extraction from cache failed for "
                + topic_filename
                + "\n:: TIP: Use --title and --content option instead"
            ),
            blink=True,
            bold=True,
            fg="bright_red",
        )

    if post_meta and not post_meta.get("content"):
        click.secho(
            ":: Warning, No available content for " + blog_topic_filename,
            fg="bright_yellow",
        )
    return post_meta


def get_config(ctx):
    config_path = os.path.join(CONFIG_DIR, ctx.current_blog, "meta.json")
    config = Config(config_path)
    return config
