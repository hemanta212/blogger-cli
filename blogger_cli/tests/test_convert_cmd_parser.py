import os
import shutil
import unittest

from tempfile import mkdtemp
from pkg_resources import resource_filename

from click.testing import CliRunner
from blogger_cli import root_dir
from blogger_cli.cli import Context
from blogger_cli.cli import cli
from blogger_cli.commands.cmd_convert import (get_files_being_converted,
    check_and_ensure_destination_dir)


class TestBasic(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()
        self.ctx = Context()
        self.export_dir = mkdtemp()
        self.blog_dir = os.path.join(self.export_dir, 'blog')
        self.index_path = os.path.join(self.blog_dir, 'index.html')
        self.runner.invoke(cli, ['addblog', 'test1'],
                    input=self.export_dir + '\nn \nn \nn \nn \nn \nn')
        self.runner.invoke(cli, ['config', '-b', 'test1',
                                 'blog_posts_dir', 'blog'])
        self.runner.invoke(cli, ['config', '-b', 'test1',
                                 'blog_images_dir', 'images'])


    def test_get_files_being_converted(self):
        resource_path = os.path.join(root_dir, 'tests', 'tests_resources')
        files = get_files_being_converted( (resource_path, ) )
        expected_files = {'html.html', 'ipynb1.ipynb', 'ipynb2.ipynb',
                        'md1.md', 'md2.md'}
        expected = {os.path.join(resource_path, i) for i in expected_files}
        self.assertEqual(expected, files)

        index_files = {'html_index.html', 'ipynb1_index.html',
                'ipynb2_index.html','md_index.html', 'topic_index.html'}
        path_join = lambda x: os.path.join(resource_path, 'index', x)
        expected_files = {path_join(i) for i in index_files}
        expected.update(expected_files)
        file1 = os.path.join(resource_path, 'html.html')
        file2 = os.path.join(resource_path, 'md1.md')
        files = get_files_being_converted((file1, file2, resource_path),
                                        recursive=True)
        self.assertEqual(expected, files)


    def tearDown(self):
        self.runner.invoke(cli, ['rmblog', 'test1'])
        shutil.rmtree(self.export_dir)


if __name__ == '__main__':
    unittest.main()
