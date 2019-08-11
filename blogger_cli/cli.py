import os
import sys
import click
from blogger_cli.cli_utils.json_writer import Config
from blogger_cli import CONFIG_DIR


class Context(object):

    def __init__(self):
        self.verbose = False
        config_path = os.path.join(CONFIG_DIR, 'blog_config.cfg')
        self.config = Config(config_path,
                             backup_dir='~/.blogger/backup/')
        self.blog_list = self.config.read(all_keys=True)
        self.config_keys = [
            'google_analytics_id', 'disqus_username', 'blog_images_dir',
            'templates_dir',  'blog_posts_dir', 'default',
            'working_dir', 'blog_dir'
        ]
        self.optional_config = [
            'meta_format', 'post_extract_list', 'index_div_name',
            'filter_post_without_title', 'working_dir_timestamp',
            'create_nbdata_file', 'delete_ipynb_meta'
        ]

        self.SUPPORTED_EXTENSIONS = ['md', 'ipynb', 'html']
        self.current_blog = ''

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            for arg in args:
                msg += ' ' + str(arg)
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
            if 'default' in cfg[i]:
                return i


pass_context = click.make_pass_decorator(Context, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          'commands'))


class ComplexCLI(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py') and \
               filename.startswith('cmd_'):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            mod = __import__('blogger_cli.commands.cmd_' + name,
                             None, None, ['cli'])
        except ImportError as e:
            return
        return mod.cli


@click.command(cls=ComplexCLI)
@click.option('-v', '--verbose', is_flag=True,
              help='enables verbose command')
@pass_context
def cli(ctx, verbose):
    '''
     A CLI tool to maintain your jupyter notebook blog. Sync, convert and upload :).
    '''
    ctx.verbose = verbose
    ctx.vlog("Started the main command")


if __name__ == "__main__":
    cli()
