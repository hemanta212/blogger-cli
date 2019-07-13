import os
import click
from blogger_cli import ROOT_DIR
from blogger_cli.cli_utils.installation import Installer, BLOGGER_CLI_VENV

@click.command('uninstall', short_help="Uninstall the custom installation")
def cli():
    """
    This command will update blogger-cli if you have installed it with custom
    installation.
   """

    custom = [False for i in  ['.blogger_cli', 'venv'] if i not in ROOT_DIR]
    if  False in custom:
       print("blogger-cli was not installed by recommended method")
       raise SystemExit("Use pip uninstall blogger-cli instead to uninstall")

    installer = Installer()
    installer.uninstall()
