import os
from datetime import datetime

import click
import dateutil.tz
from feedgen.feed import FeedGenerator

from blogger_cli import BACKUP_DIR
from blogger_cli.commands.feed_utils.feedprocessor import FeedProcessor


def setup_new_file(file_path, feed_type):
    setup = __load_setup()
    feed = __init_feed(setup)
    init_feed_file(feed, file_path, feed_type)


def __load_setup():
    click.echo("Use n to skip through options! [*] marked field are REQUIRED")
    key_help_map = {
        "id": "Website URL of this feed. eg: https://mywebsite.com [*]",
        "title": "Title for the feed. eg. Coding adventures [*]",
        "subtitle": "Subtitle for the feed eg: A documentation of my coding journey",
        "author": "Name of the author of feed [*]",
        "logo": "Image of logo in URL format.",
        "link": "URL of this feed. eg: https://mywebsite.com/feed [*]",
    }
    config_keys = ["id", "title", "subtitle", "author", "link", "logo"]
    setup = {}
    for config_key in config_keys:
        hint = " - {0}".format(key_help_map[config_key])
        value = click.prompt(config_key + hint)
        if value.strip() == "":
            setup[config_key] = None
        elif value != "n":
            setup[config_key] = value
    return setup


def __init_feed(setup):
    feed = FeedGenerator()
    feed.id(setup.get("id"))
    feed.title(setup.get("title"))
    feed.subtitle(setup.get("subtitle"))
    feed.author({"name": setup.get("name"), "email": setup.get("email")})
    feed.link(href=setup.get("link"), rel="self")
    feed.logo(setup.get("logo"))
    return feed


def init_feed_file(feed, feed_file_path, feed_type):
    backup_name = os.path.join(BACKUP_DIR, os.path.basename(feed_file_path))
    if os.path.exists(feed_file_path):
        os.rename(feed_file_path, backup_name)
        filetype = {"atom": feed.atom_file, "rss": feed.rss_file}
        try:
            filetype[feed_type](feed_file_path)
        except ValueError:
            click.secho(
                ":: ERROR required fields were not filled. Aborting..",
                bold=True,
                blink=True,
                fg="bright_red",
            )
            raise SystemExit()


def validate_entry(ctx, post_meta):
    sitelink = ensure_sitelink(ctx)
    required = ["title", "link"]
    missing = []
    for key in required:
        if not post_meta.get(key):
            missing.append(key)

    if not missing:
        post_meta["link"] = sitelink + "/" + post_meta["link"]
        return post_meta

    ctx.log(":: Missing required fields: " + ", ".join(missing))
    for key in missing:
        value = input(key + " [*] - ")
        post_meta[key] = value

    return validate_entry(ctx, post_meta)


def ensure_sitelink(ctx):
    blog = ctx.current_blog
    site_key = blog + ": site_url"
    site_link = ctx.config.read(key=site_key)
    if not site_link:
        site_link = input("Website url: ")
        ctx.config.write(site_key, site_link)
    return site_link


def add_entry(ctx, feed_file, entry):
    # Get metadata from meta.json file in config
    updated_time = str(datetime.now(dateutil.tz.tzutc()))
    entry_id = ctx.current_blog + "-" + updated_time
    entry["updated"] = updated_time
    entry["id"] = entry_id

    feed_processor = FeedProcessor(feed_file)
    xml = feed_processor.add_entry(entry)
    feed_processor.write_to_file(xml)
