import os
import unittest
from blogger_cli.cli import cli
from pkg_resources import resource_filename
from conversion_utils import setUp, tearDown, read_file


class TestIpynb(unittest.TestCase):
    def setUp(self):
        setUp(self)

    def test_ipynb(self):
        ipynb1_path = resource_filename('blogger_cli',
                    'tests/tests_resources/ipynb1.ipynb')
        test_index_path = resource_filename('blogger_cli',
                    'tests/tests_resources/index/ipynb1_index.html')

        result = self.runner.invoke(cli, ['convert', '-b', 'test1',
                                ipynb1_path, '-v'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(['blog', 'images'],
                        os.listdir(self.export_dir))
        expected_files = {'index.html', 'ipynb1.html', 'ipynb1.ipynb'}
        self.assertEqual(expected_files,
                        set(os.listdir(self.blog_dir)))
        #os.system('cp '+ self.index_path+ ' '+ test_index_path)
        self.assertEqual(read_file(self.index_path), read_file(test_index_path))


    def test_html(self):
        self.maxDiff = None
        html_path = resource_filename('blogger_cli',
                    'tests/tests_resources/html.html')
        test_index_path = resource_filename('blogger_cli',
                    'tests/tests_resources/index/html_index.html')

        result = self.runner.invoke(cli, ['convert', '-b', 'test1',
                                html_path, '-v'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(['blog', 'images'], os.listdir(self.export_dir))

        self.assertEqual(['html.html', 'index.html'],
                        os.listdir(self.blog_dir))
        self.assertEqual(read_file(self.index_path), read_file(test_index_path))


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
        tearDown(self)


if __name__ == '__main__':
    unittest.main()
