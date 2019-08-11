import os

__version__ = '1.1.0'
ROOT_DIR = os.path.join(os.path.split(__file__)[0])
RESOURCE_DIR = os.path.join(os.path.split(__file__)[0], 'resources')

HOME = os.path.expanduser('~')
CONFIG_DIR = os.path.join(HOME, '.config', 'blogger_cli')
