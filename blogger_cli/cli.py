import os
import sys

import click

from blogger_cli import BACKUP_DIR, CONFIG_DIR
from blogger_cli.cli_utils.json_writer import Config


class Context(object):
    def __init__(self):
        self.verbose = False
        config_path = os.path.join(CONFIG_DIR, "blog_config.cfg")
        self.config = Config(config_path, backup_dir=BACKUP_DIR)
        self.blog_list = self.config.read(all_keys=True)
        self.config_keys = [
            "google_analytics_id",
            "disqus_username",
            "blog_images_dir",
            "templates_dir",
            "blog_posts_dir",
            "default",
            "working_dir",
            "blog_dir",
        ]
        self.optional_config = [
            "meta_format",  # comment format in metadata
            "post_extract_list",  # resource to extract from file
            "index_div_name",  # div name of posts list in blog index
            "filter_post_without_title",  # filter titleless post from indexing
            "working_dir_timestamp",  # Timestamp of last checked working dir
            "create_nbdata_file",  # Flag for creating nbdata file
            "delete_ipynb_meta",  # Delete metadata in ipynb file after reading
            "feed_file",  # Path of feed file
            "site_url",  # URL of website [for building feed links].
            "md_summary_limit",  # No of charectar to include in md summary.
            "ipynb_summary_limit",  # ipynb char limit or Cell no to extract
        ]

        self.SUPPORTED_EXTENSIONS = ["md", "ipynb", "html"]
        self.current_blog = ""

    def log(self, msg, *args):
        """Logs a message to stderr."""
        msg = str(msg)
        if args:
            for arg in args:
                msg += " " + str(arg)

        message = msg.lower() if msg else ""

        # handle basic coloring
        if "error" in message:
            click.secho(msg, file=sys.stderr, bold=True, blink=True, fg="bright_red")
        elif "warning" in message or "!" in message:
            click.secho(msg, file=sys.stderr, bold=True, fg="bright_yellow")
        elif "converting" in message or "adding" in message:
            click.secho(msg, file=sys.stderr, fg="blue")
        elif "finished" in message or "done" in message or "successfully" in message:
            click.secho(msg, file=sys.stderr, fg="green")

        else:
            click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)

    def blog_exists(self, blog):
        return False if not self.config.read(key=blog) else True

    @property
    def default_blog(self):
        cfg = self.config.get_dict()
        for i in cfg:
            if "default" in cfg[i]:
                return i


pass_context = click.make_pass_decorator(Context, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "commands"))


class ComplexCLI(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith(".py") and filename.startswith("cmd_"):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode("ascii", "replace")
            mod = __import__("blogger_cli.commands.cmd_" + name, None, None, ["cli"])
        except ImportError as e:
            return
        return mod.cli


@click.command(cls=ComplexCLI)
@click.option("-v", "--verbose", is_flag=True, help="enables verbose command")
@pass_context
def cli(ctx, verbose):
    """
     A CLI tool to maintain your jupyter notebook blog.
    """
    ctx.verbose = verbose


if __name__ == "__main__":
    cli()
