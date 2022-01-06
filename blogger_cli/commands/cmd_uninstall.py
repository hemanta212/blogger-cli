import os
import click
import shutil
from pkg_resources import resource_filename
from blogger_cli import ROOT_DIR, CONFIG_DIR
from blogger_cli.cli_utils.installation import Installer, WINDOWS, BLOGGER_CLI_HOME


@click.command("uninstall", short_help="Uninstall the custom installation")
def cli():
    """
    This command will update blogger-cli if you have installed it with custom
    installation.
   """

    custom = [False for i in [".blogger_cli", "venv"] if i not in ROOT_DIR]
    if False in custom:
        click.secho(
            "blogger-cli was not installed by recommended method",
            ":: ERROR use pip uninstall blogger-cli instead to uninstall",
            bold=True,
            fg="bright_red",
        )
        raise SystemExit()

    if not WINDOWS:
        installer = Installer()
        installer.uninstall()
        return

    installer = Installer()
    installer.remove_from_windows_path()
    new_file_path = os.path.join(CONFIG_DIR, "blogger_installer.py")
    installer_location = "cli_utils/installation.py"
    installer_path = resource_filename("blogger_cli", installer_location)
    shutil.copyfile(installer_path, new_file_path)

    msg = (
        "Please run this command manually to Uninstall:\n",
        "python",
        new_file_path,
        "--uninstall",
    )
    click.secho(msg, fg="green")
