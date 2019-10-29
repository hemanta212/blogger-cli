import os
import click

__version__ = "1.2.1"
ROOT_DIR = os.path.join(os.path.split(__file__)[0])
RESOURCE_DIR = os.path.join(os.path.split(__file__)[0], "resources")

CONFIG_DIR = click.get_app_dir("blogger_cli")
BACKUP_DIR = os.path.join(CONFIG_DIR, "backup")

for DIR in (CONFIG_DIR, BACKUP_DIR):
    if not os.path.exists(DIR):
        os.makedirs(DIR)
