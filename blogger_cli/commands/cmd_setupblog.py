from pathlib import Path
import click
from blogger_cli.cli import pass_context


@click.command("setupblog", short_help="Register a new blog")
@click.argument("blog")
@click.option("-v", "--verbose", is_flag=True)
@pass_context
def cli(ctx, blog, verbose):
    """ Load a setup procedure to a blog.\n
    Usage:\n
        blogger setupblog blogname
    """
    ctx.verbose = verbose
    if not ctx.blog_exists(blog):
        ctx.log("Blog doesnot exist!")
    else:
        ctx.log("Setting up blog")
        setup(ctx, blog)


def setup(ctx, blog):
    ctx.log("Use n to skip through options!")
    blog_attrs = ctx.config.read(key=blog)
    key_help_map = {
        "blog_dir": "Path of your blog",
        "blog_posts_dir": "Blog's posts folder (relative to blog_dir)",
        "blog_images_dir": "Blog's images folder (relative to blog_dir)",
        "templates_dir": "Path of folder of your custom templates (if any)",
        "working_dir": "Folder where keep your md, ipynb, html files",
        "google_analytics_id": "It is in the snippet provided by google eg:UA-039224021-1",
        "disqus_username": "It is in url of your disqus account eg: https://username.disqus.com/",
    }

    messages = []
    success = True
    for k, v in sorted(blog_attrs.items()):
        try:
            hint = " - {0}".format(key_help_map[k])
            value = click.prompt(k + hint, default=v)

            if value.strip() == "":
                ctx.config.write("{0}:{1}".format(blog, k), None)

            elif value != "n":
                if k in ["blog_dir", "working_dir", "templates_dir"]:
                    value, msg = ensure_and_expand_dir(value)
                    if msg:
                        success = False
                        messages.append(msg)

                ctx.config.write("{0}:{1}".format(blog, k), value)

        except KeyError:
            # The option is not supposed to be setup by user like defaultblog
            pass

    for message in messages:
        ctx.log("\n", message)
    if success:
        ctx.log("Blog setup completed succesfully")


def ensure_and_expand_dir(dir):
    folder = Path(dir)
    try:
        full_path = str(folder.expanduser().resolve())
    except FileNotFoundError as E:
        return None, "ERROR:" + str(E)

    return full_path, ""
