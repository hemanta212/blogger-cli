import os
import shutil
import unittest
from click.testing import CliRunner
from blogger_cli.cli import cli
from blogger_cli import root_dir
from blogger_cli.tests.messages import BloggerMessage as BM
from pkg_resources import resource_filename


class TestBasic(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()
        self.export_dir = os.path.expanduser('~/.blogger_tmp/')
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


    def test_topic(self):
        self.maxDiff = None

        files_path = os.path.join(root_dir, 'tests', 'tests_resources')
        test_index_path = resource_filename('blogger_cli',
                    'tests/tests_resources/index/topic_index.html')

        result = self.runner.invoke(cli, ['convert', '-b', 'test1',
                                files_path, '--topic', 'test1'])

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(['blog', 'images'], os.listdir(self.export_dir))

        blog_dir_files = ['index.html', 'meta', 'test1']
        self.assertEqual(set(blog_dir_files), set(os.listdir(self.blog_dir)))

        meta_dir = os.path.join(self.blog_dir, 'meta')
        meta_topic_files = ['md2.html', 'md2.md']
        self.assertEqual(set(meta_topic_files), set(os.listdir(meta_dir)))

        test1_dir = os.path.join(self.blog_dir, 'test1')
        test1_topic_files = ['html.html', 'md1.html', 'md1.md', 'ipynb2.html',
                            'ipynb2.ipynb', 'ipynb1.html', 'ipynb1.ipynb']
        self.assertEqual(set(test1_topic_files), set(os.listdir(test1_dir)))
        os.system('cp '+ self.index_path+ ' '+ test_index_path)
        #self.assertEqual(self.read_file(self.index_path), self.read_file(test_index_path))


    def tearDown(self):
        self.runner.invoke(cli, ['rmblog', 'test1'])
        shutil.rmtree(self.export_dir)


if __name__ == '__main__':
    unittest.main()
