import os
import shutil
import unittest
from tempfile import tempdir, tempfile

from blogger_cli.commands.cmd_convert import (get_files_being_converted,
    get_all_files, check_and_ensure_destination_dir)
from blogger_cli import root_dir
from blogger_cli.cli import Context
from pkg_resources import resource_filename


class TestBasic(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()
        self.ctx = Context()
        self.export_dir = tempdir
        self.blog_dir = os.path.join(self.export_dir, 'blog')
        self.index_path = os.path.join(self.blog_dir, 'index.html')
        self.runner.invoke(cli, ['addblog', 'test1'],
                    input=self.export_dir + '\nn \nn \nn \nn \nn \nn')
        self.runner.invoke(cli, ['config', '-b', 'test1',
                                 'blog_posts_dir', 'blog'])
        self.runner.invoke(cli, ['config', '-b', 'test1',
                                 'blog_images_dir', 'images'])

    def test_get_files_being_converted(self):
         resource_path = resource_filename('blogger_cli',
                    'tests/tests_resources/')
        files = get_files_being_converted(resource_path)
        expected_files = {'html.html', 'ipynb1.ipynb', 'ipynb2.ipynb', 'md1.md'

