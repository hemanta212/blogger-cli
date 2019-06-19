import os
import shutil
from click.testing import CliRunner
from blogger_cli.cli import cli
from pkg_resources import resource_filename


def setUp(self):
    self.runner = CliRunner()
    HOME_DIR = os.path.expanduser('~')
    self.export_dir = os.path.join(HOME_DIR, '.blogger_tmp')
    self.blog_dir = os.path.join(self.export_dir, 'blog')
    self.index_path = os.path.join(self.blog_dir, 'index.html')
    self.runner.invoke(cli, ['addblog', 'test1'],
                input=self.export_dir + '\nn \nn \nn \nn \nn \nn')
    self.runner.invoke(cli, ['config', '-b', 'test1',
                             'blog_posts_dir', 'blog'])
    self.runner.invoke(cli, ['config', '-b', 'test1',
                             'blog_images_dir', 'images'])
    self.runner.invoke(cli, ['export', '-b', 'test1', 'blog_index',
                            '-o', 'blog'])

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as rf:
        data = rf.read()
        return data
        rf.close()

def tearDown(self):
    self.runner.invoke(cli, ['rmblog', 'test1'])
    shutil.rmtree(self.export_dir)
