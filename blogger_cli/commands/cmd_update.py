import os
import click
from blogger_cli import ROOT_DIR
from blogger_cli.cli_utils.installation import Installer

@click.command('update', short_help="Update the custom installation")
@click.option('-f', '--force', is_flag=True)
@click.option('--version', is_flag=True)
@click.option('-y', 'accept_all',  is_flag=True)
def cli(version, force, accept_all):
    """
    This command will update blogger-cli if you have installed it with custom
    installation.
   """

    custom = [False for i in  ['.blogger_cli', 'venv'] if i not in ROOT_DIR]
    if  False in custom:
       print("blogger-cli was not installed by recommended method")
       raise SystemExit("Use pip install --upgrade blogger-cli instead to upgrade")

    installer = Installer(
        version=version,
        force=force,
        accept_all=accept_all
    )
    installer.run()
