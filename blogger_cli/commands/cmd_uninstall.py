import os
import click
from pkg_resources import resource_filename
from blogger_cli import ROOT_DIR, CONFIG_DIR
from blogger_cli.cli_utils.installation import (Installer, WINDOWS,
                                                BLOGGER_CLI_HOME)

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

    if not WINDOWS:
        installer = Installer()
        installer.uninstall()
        return

    installer = Installer()
    installer.remove_from_windows_path()
    new_file_path = os.path.join(CONFIG_DIR, 'blogger_installer.py')
    installer_location = 'cli_utils/installation.py'
    installer_path = resource_filename('blogger_cli', installer_location)
    shutil.copyfile(installer_path, new_file_path)
    try:
        os.system('python ' + new_file_path + ' --uninstall')
    except:
        print("Please manually remove the blogger dir at", BLOGGER_CLI_HOME)
