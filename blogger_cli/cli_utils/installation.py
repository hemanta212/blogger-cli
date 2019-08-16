"""
This script will install blogger-cli and its dependencies
in isolation from the rest of the system.

It does, in order:
  - Downloads the latest stable version of blogger-cli.
  - Downloads all its dependencies in the blogger-cli/venv directory.
  - Copies it and all extra files in $BLOGGER_CLI_HOME.
  - Updates the PATH in a system-specific way.

There will be a `blogger` script that will be installed in $BLOGGER_CLI_HOME/bin
"""

import argparse
import os
import platform
import shutil
import stat
import subprocess
import sys

from contextlib import closing
from io import UnsupportedOperation

try:
    from urllib.request import Request
    from urllib.request import urlopen
except ImportError:
    from urllib2 import Request
    from urllib2 import urlopen

try:
    input = raw_input
except NameError:
    pass


try:
    try:
        import winreg
    except ImportError:
        import _winreg as winreg
except ImportError:
    winreg = None


WINDOWS = sys.platform.startswith("win") or (sys.platform == "cli" and os.name == "nt")


FOREGROUND_COLORS = {
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "white": 37,
}

BACKGROUND_COLORS = {
    "black": 40,
    "red": 41,
    "green": 42,
    "yellow": 43,
    "blue": 44,
    "magenta": 45,
    "cyan": 46,
    "white": 47,
}

OPTIONS = {"bold": 1, "underscore": 4, "blink": 5, "reverse": 7, "conceal": 8}


def style(fg, bg, options):
    codes = []

    if fg:
        codes.append(FOREGROUND_COLORS[fg])

    if bg:
        codes.append(BACKGROUND_COLORS[bg])

    if options:
        if not isinstance(options, (list, tuple)):
            options = [options]

        for option in options:
            codes.append(OPTIONS[option])

    return "\033[{}m".format(";".join(map(str, codes)))


STYLES = {
    "info": style("green", None, None),
    "comment": style("yellow", None, None),
    "error": style("red", None, None),
    "warning": style("yellow", None, None),
}


def is_decorated():
    if platform.system().lower() == "windows":
        return (
            os.getenv("ANSICON") is not None
            or os.getenv("ConEmuANSI") == "ON"
            or os.getenv("Term") == "xterm"
        )

    if not hasattr(sys.stdout, "fileno"):
        return False

    try:
        return os.isatty(sys.stdout.fileno())
    except UnsupportedOperation:
        return False


def is_interactive():
    if not hasattr(sys.stdin, "fileno"):
        return False

    try:
        return os.isatty(sys.stdin.fileno())
    except UnsupportedOperation:
        return False


def colorize(style, text):
    if not is_decorated():
        return text

    return "{}{}\033[0m".format(STYLES[style], text)


def string_to_bool(value):
    value = value.lower()

    return value in {"true", "1", "y", "yes"}


def expanduser(path):
    """
    Expand ~ and ~user constructions.

    Includes a workaround for http://bugs.python.org/issue14768
    """
    expanded = os.path.expanduser(path)
    if path.startswith("~/") and expanded.startswith("//"):
        expanded = expanded[1:]

    return expanded


HOME = expanduser("~")
LINUX_HOME = os.path.join(HOME, "local", ".blogger_cli")
WINDOWS_HOME = os.path.join(HOME, ".blogger_cli")
BLOGGER_CLI_HOME = WINDOWS_HOME if WINDOWS else LINUX_HOME
BLOGGER_CLI_BIN = os.path.join(BLOGGER_CLI_HOME, "bin")
BLOGGER_CLI_ENV = os.path.join(BLOGGER_CLI_HOME, "env")
BLOGGER_CLI_VENV = os.path.join(BLOGGER_CLI_HOME, "venv")
BLOGGER_CLI_VENV_BACKUP = os.path.join(BLOGGER_CLI_HOME, "venv-backup")


BIN = """#!{python_path}
from blogger_cli.cli import cli

if __name__ == "__main__":
    cli()
"""

BAT = '@echo off\r\n{python_path} "{blogger_cli_bin}" %*\r\n'


PRE_MESSAGE = """# Welcome to {blogger-cli}!

This will download and install the latest version of {blogger-cli},
a ipynb converter and blog manager.

It will add the `blogger` command to {blogger-cli}'s bin directory, located at:

{blogger_cli_home_bin}

{platform_msg}

You can uninstall at any time by executing this script
with the --uninstall option,
and these changes will be reverted.
"""

PRE_UNINSTALL_MESSAGE = """# We are sorry to see you go!

This will uninstall {blogger-cli}.

It will remove the `blogger` command from {blogger-cli}'s bin directory, located at:

{blogger_cli_home_bin}

This will also remove {blogger-cli} from your system's PATH.
"""


PRE_MESSAGE_UNIX = """This path will then be added to your `PATH` environment variable by
modifying the profile file{plural} located at:

{rcfiles}"""


PRE_MESSAGE_WINDOWS = """This path will then be added to your `PATH` environment variable by
modifying the `HKEY_CURRENT_USER/Environment/PATH` registry key."""

PRE_MESSAGE_NO_MODIFY_PATH = """This path needs to be in your `PATH` environment variable,
but will not be added automatically."""

POST_MESSAGE_UNIX = """{blogger-cli} is installed now. Great!

To get started you need {blogger-cli}'s bin directory ({blogger_cli_home_bin}) in your `PATH`
environment variable. Next time you log in this will be done
automatically.

You have to run blogger-cli using the 'blogger' command!
If 'blogger' command doesnot work place {linux_addition} in your bashrc/bash_profile

To configure your current shell run `source {blogger_cli_home_env}`
"""

POST_MESSAGE_WINDOWS = """{blogger-cli} is installed now. Great!

To get started you need blogger-cli's bin directory ({blogger_cli_home_bin}) in your `PATH`
environment variable. Future applications will automatically have the
correct environment, but you may need to restart your current shell.
You have to run blogger-cli using the 'blogger' command!
"""

POST_MESSAGE_WINDOWS_NO_MODIFY_PATH = """{blogger-cli} is installed now. Great!

To get started you need Blogger-cli's bin directory ({blogger_cli_home_bin}) in your `PATH`
environment variable. This has not been done automatically.

You have to run blogger-cli using the 'blogger' command!
"""


class Installer:

    CURRENT_PYTHON = sys.executable
    CURRENT_PYTHON_VERSION = sys.version_info[:2]

    def __init__(self, version=None, force=False, accept_all=False):
        self._version = version
        self._force = force
        self._modify_path = True
        self._accept_all = accept_all

    def run(self):
        self.display_pre_message()
        self.ensure_python_version()
        self.ensure_home()

        try:
            self.install()
        except subprocess.CalledProcessError as e:
            print(colorize("error", "An error has occured: {}".format(str(e))))
            print(e.output.decode())

            return e.returncode

        self.display_post_message(self._version)

        return 0

    def uninstall(self):
        self.display_pre_uninstall_message()

        if not self.customize_uninstall():
            return

        self.remove_home()
        self.remove_from_path()

    def ensure_python_version(self):
        major, minor = self.CURRENT_PYTHON_VERSION
        if major < 3 or minor < 5:
            print("SORRY BLOGGER CLI IS NOT SUPPORTED ONLY FOR 3.5 AND ABOVE!")
            sys.exit(1)

    def customize_uninstall(self):
        if not self._accept_all:
            print()

            uninstall = (
                input("Are you sure you want to uninstall Blogger-cli? (y/[n]) ") or "n"
            )
            if uninstall.lower() not in {"y", "yes"}:
                return False

            print("")

        return True

    def ensure_home(self):
        """
        Ensures that $BLOGGER_CLI_HOME exists or create it.
        """
        if not os.path.exists(BLOGGER_CLI_HOME):
            os.makedirs(BLOGGER_CLI_HOME, 0o755)

    def remove_home(self):
        """
        Removes $BLOGGER_CLI_HOME.
        """
        if not os.path.exists(BLOGGER_CLI_HOME):
            return

        shutil.rmtree(BLOGGER_CLI_HOME)

    def install(self):
        """
        Installs Blogger-cli in $BLOGGER_CLI_HOME.
        """
        version = self._version if self._version else "Latest"
        print("Installing version: " + colorize("info", version))

        self.make_venv()
        self.make_bin()
        self.make_env()
        self.update_path()

        return 0

    def make_venv(self):
        """
        Packs everything into a single lib/ directory.
        """
        if os.path.exists(BLOGGER_CLI_VENV_BACKUP):
            shutil.rmtree(BLOGGER_CLI_VENV_BACKUP)

        # Backup the current installation
        if os.path.exists(BLOGGER_CLI_VENV):
            shutil.copytree(BLOGGER_CLI_VENV, BLOGGER_CLI_VENV_BACKUP)
            if self._force:
                shutil.rmtree(BLOGGER_CLI_VENV)

        try:
            self._make_venv()
        except Exception:
            if not os.path.exists(BLOGGER_CLI_VENV_BACKUP):
                raise

            shutil.copytree(BLOGGER_CLI_VENV_BACKUP, BLOGGER_CLI_VENV)
            shutil.rmtree(BLOGGER_CLI_VENV_BACKUP)

            raise
        finally:
            if os.path.exists(BLOGGER_CLI_VENV_BACKUP):
                shutil.rmtree(BLOGGER_CLI_VENV_BACKUP)

    def _make_venv(self):
        global BIN, BAT
        if not os.path.exists(BLOGGER_CLI_VENV):
            import venv

            print("Making virtualenv in", BLOGGER_CLI_VENV)
            venv.create(BLOGGER_CLI_VENV, with_pip=True)

        windows_path = os.path.join(BLOGGER_CLI_VENV, "Scripts", "python")
        linux_path = os.path.join(BLOGGER_CLI_VENV, "bin", "python")
        new_python = windows_path if WINDOWS else linux_path
        new_pip = new_python + " -m pip"

        if self._version:
            install_cmd = new_pip + " install blogger-cli==" + self._version
        else:
            install_cmd = new_pip + " install -U blogger-cli"

        BIN = BIN.format(python_path=new_python)
        BAT = BAT.format(python_path=new_python, blogger_cli_bin="{blogger_cli_bin}")

        os.system(install_cmd)

    def make_bin(self):
        if not os.path.exists(BLOGGER_CLI_BIN):
            os.mkdir(BLOGGER_CLI_BIN, 0o755)

        if WINDOWS:
            with open(os.path.join(BLOGGER_CLI_BIN, "blogger.bat"), "w") as f:
                f.write(
                    BAT.format(
                        blogger_cli_bin=os.path.join(
                            BLOGGER_CLI_BIN, "blogger"
                        ).replace(os.environ["USERPROFILE"], "%USERPROFILE%")
                    )
                )

        with open(os.path.join(BLOGGER_CLI_BIN, "blogger"), "w") as f:
            f.write(BIN)

        if not WINDOWS:
            # Making the file executable
            st = os.stat(os.path.join(BLOGGER_CLI_BIN, "blogger"))
            os.chmod(
                os.path.join(BLOGGER_CLI_BIN, "blogger"), st.st_mode | stat.S_IEXEC
            )

    def make_env(self):
        if WINDOWS:
            return

        with open(os.path.join(BLOGGER_CLI_HOME, "env"), "w") as f:
            f.write(self.get_export_string())

    def update_path(self):
        """
        Tries to update the $PATH automatically.
        """
        if WINDOWS:
            return self.add_to_windows_path()

        # Updating any profile we can on UNIX systems
        export_string = self.get_export_string()

        self.linux_addition = "\n{}\n".format(export_string)

        updated = []
        profiles = self.get_unix_profiles()
        for profile in profiles:
            if not os.path.exists(profile):
                continue

            with open(profile, "r") as f:
                content = f.read()

            if self.linux_addition not in content:
                with open(profile, "a") as f:
                    f.write(self.linux_addition)

                updated.append(os.path.relpath(profile, HOME))

    def add_to_windows_path(self):
        try:
            old_path = self.get_windows_path_var()
        except WindowsError:
            old_path = None

        if old_path is None:
            print(
                colorize(
                    "warning",
                    "Unable to get the PATH value. It will not be updated automatically",
                )
            )
            self._modify_path = False

            return

        new_path = BLOGGER_CLI_BIN
        if BLOGGER_CLI_BIN in old_path:
            old_path = old_path.replace(BLOGGER_CLI_BIN + ";", "")

        if old_path:
            new_path += ";"
            new_path += old_path

        self.set_windows_path_var(new_path)

    def get_windows_path_var(self):
        with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as root:
            with winreg.OpenKey(root, "Environment", 0, winreg.KEY_ALL_ACCESS) as key:
                path, _ = winreg.QueryValueEx(key, "PATH")

                return path

    def set_windows_path_var(self, value):
        import ctypes

        with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as root:
            with winreg.OpenKey(root, "Environment", 0, winreg.KEY_ALL_ACCESS) as key:
                winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, value)

        # Tell other processes to update their environment
        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x1A

        SMTO_ABORTIFHUNG = 0x0002

        result = ctypes.c_long()
        SendMessageTimeoutW = ctypes.windll.user32.SendMessageTimeoutW
        SendMessageTimeoutW(
            HWND_BROADCAST,
            WM_SETTINGCHANGE,
            0,
            u"Environment",
            SMTO_ABORTIFHUNG,
            5000,
            ctypes.byref(result),
        )

    def remove_from_path(self):
        if WINDOWS:
            return self.remove_from_windows_path()

        return self.remove_from_unix_path()

    def remove_from_windows_path(self):
        path = self.get_windows_path_var()
        blogger_cli_path = BLOGGER_CLI_BIN
        if blogger_cli_path in path:
            path = path.replace(BLOGGER_CLI_BIN + ";", "")

            if blogger_cli_path in path:
                path = path.replace(BLOGGER_CLI_BIN, "")

        self.set_windows_path_var(path)

    def remove_from_unix_path(self):
        # Updating any profile we can on UNIX systems
        export_string = self.get_export_string()

        addition = "{}\n".format(export_string)

        profiles = self.get_unix_profiles()
        for profile in profiles:
            if not os.path.exists(profile):
                continue

            with open(profile, "r") as f:
                content = f.readlines()

            if addition not in content:
                continue

            new_content = []
            for line in content:
                if line == addition:
                    if new_content and not new_content[-1].strip():
                        new_content = new_content[:-1]

                    continue

                new_content.append(line)

            with open(profile, "w") as f:
                f.writelines(new_content)

    def get_export_string(self):
        path = BLOGGER_CLI_BIN.replace(os.getenv("HOME", ""), "$HOME")
        export_string = 'export PATH="{}:$PATH"'.format(path)

        return export_string

    def get_unix_profiles(self):
        profiles = [os.path.join(HOME, ".profile")]

        shell = os.getenv("SHELL", "")
        if "zsh" in shell:
            zdotdir = os.getenv("ZDOTDIR", HOME)
            profiles.append(os.path.join(zdotdir, ".zprofile"))

        bash_profile = os.path.join(HOME, ".bash_profile")
        if os.path.exists(bash_profile):
            profiles.append(bash_profile)

        return profiles

    def display_pre_message(self):
        if WINDOWS:
            home = BLOGGER_CLI_BIN.replace(
                os.getenv("USERPROFILE", ""), "%USERPROFILE%"
            )
        else:
            home = BLOGGER_CLI_BIN.replace(os.getenv("HOME", ""), "$HOME")

        kwargs = {
            "blogger-cli": colorize("info", "blogger-cli"),
            "blogger_cli_home_bin": colorize("comment", home),
        }

        if not self._modify_path:
            kwargs["platform_msg"] = PRE_MESSAGE_NO_MODIFY_PATH
        else:
            if WINDOWS:
                kwargs["platform_msg"] = PRE_MESSAGE_WINDOWS
            else:
                profiles = [
                    colorize("comment", p.replace(os.getenv("HOME", ""), "$HOME"))
                    for p in self.get_unix_profiles()
                ]
                kwargs["platform_msg"] = PRE_MESSAGE_UNIX.format(
                    rcfiles="\n".join(profiles), plural="s" if len(profiles) > 1 else ""
                )

        print(PRE_MESSAGE.format(**kwargs))

    def display_pre_uninstall_message(self):
        home_bin = BLOGGER_CLI_BIN
        if WINDOWS:
            home_bin = home_bin.replace(os.getenv("USERPROFILE", ""), "%USERPROFILE%")
        else:
            home_bin = home_bin.replace(os.getenv("HOME", ""), "$HOME")

        kwargs = {
            "blogger-cli": colorize("info", "blogger-cli"),
            "blogger_cli_home_bin": colorize("comment", home_bin),
        }

        print(PRE_UNINSTALL_MESSAGE.format(**kwargs))

    def display_post_message(self, version):
        print("")

        kwargs = {
            "blogger-cli": colorize("info", "blogger-cli"),
            "version": colorize("comment", version),
        }

        if WINDOWS:
            message = POST_MESSAGE_WINDOWS
            if not self._modify_path:
                message = POST_MESSAGE_WINDOWS_NO_MODIFY_PATH

            blogger_cli_home_bin = BLOGGER_CLI_BIN.replace(
                os.getenv("USERPROFILE", ""), "%USERPROFILE%"
            )
        else:
            message = POST_MESSAGE_UNIX
            blogger_cli_home_bin = BLOGGER_CLI_BIN.replace(
                os.getenv("HOME", ""), "$HOME"
            )
            kwargs["blogger_cli_home_env"] = colorize(
                "comment", BLOGGER_CLI_ENV.replace(os.getenv("HOME", ""), "$HOME")
            )

            kwargs["linux_addition"] = self.linux_addition

        kwargs["blogger_cli_home_bin"] = colorize("comment", blogger_cli_home_bin)
        print(message.format(**kwargs))

    def call(self, *args):
        return subprocess.check_output(args, stderr=subprocess.STDOUT)

    def _get(self, url):
        request = Request(url, headers={"User-Agent": "Python Blogger-cli"})

        with closing(urlopen(request)) as r:
            return r.read()


def main():
    parser = argparse.ArgumentParser(
        description="Installs the latest (or given) version of blogger-cli"
    )
    parser.add_argument("--version", dest="version")
    parser.add_argument(
        "-f", "--force", dest="force", action="store_true", default=False
    )
    parser.add_argument(
        "-y", "--yes", dest="accept_all", action="store_true", default=False
    )
    parser.add_argument(
        "--uninstall", dest="uninstall", action="store_true", default=False
    )

    args = parser.parse_args()

    installer = Installer(
        version=args.version or os.getenv("BLOGGER_CLI_VERSION"),
        force=args.force,
        accept_all=args.accept_all
        or string_to_bool(os.getenv("BLOGGER_CLI_ACCEPT", "0"))
        or not is_interactive(),
    )

    if args.uninstall or string_to_bool(os.getenv("BLOGGER_CLI_UNINSTALL", "0")):
        return installer.uninstall()

    return installer.run()


if __name__ == "__main__":
    sys.exit(main())
