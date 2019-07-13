import os
import click
from pkg_resources import resource_filename
from blogger_cli import ROOT_DIR, CONFIG_DIR
from blogger_cli.cli_utils.installation import (Installer, WINDOWS,
                                                BLOGGER_CLI_HOME)

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

    if not WINDOWS or not force:
        installer = Installer(
        version=version,
        force=force,
        accept_all=accept_all
        )
        installer.run()
        return

    new_file_path = os.path.join(CONFIG_DIR, 'blogger_installer.py')
    installer_location = 'cli_utils/installation.py'
    installer_path = resource_filename('blogger_cli', installer_location)
    shutil.copyfile(installer_path, new_file_path)

    last_string = ' -f '
    if version:
        last_string += ' --version '+ version
    if accept_all:
        last_string += ' -y'

    try:
        os.system('python ' + new_file_path + last_string)
    except:
        print("CRITICAL ERROR Please manually remove the blogger dir at",
             BLOGGER_CLI_HOME, "And run file at", new_file_path,
             "with python3 to install latest blogger-cli")

