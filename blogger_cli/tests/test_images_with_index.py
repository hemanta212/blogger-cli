import os
import unittest
from blogger_cli.cli import cli
from pkg_resources import resource_filename
from conversion_utils import setUp, tearDown, read_file


class TestConversion(unittest.TestCase):
    def setUp(self):
        setUp(self)

    test = '''\
    def test_ipynb_images_and_index(self):
        ipynb1_path = resource_filename('blogger_cli',
                    'tests/tests_resources/ipynb1.ipynb')
        self.runner.invoke(cli, ['convert', '-b', 'test1',
                                ipynb1_path, '-v'])
        ipynb2_path = resource_filename('blogger_cli',
                    'tests/tests_resources/ipynb2.ipynb')
        test_index_path = resource_filename('blogger_cli',
                    'tests/tests_resources/index/ipynb2_index.html')

        result = self.runner.invoke(cli, ['setdefault', 'test1'])
        result = self.runner.invoke(cli, ['convert', ipynb2_path, '-v'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(['blog', 'images'],
                        os.listdir(self.export_dir))
        expected_files = {'index.html', 'ipynb1.html', 'ipynb1.ipynb',
                         'ipynb2.html', 'ipynb2.ipynb'}
        self.assertEqual(expected_files,
                        set(os.listdir(self.blog_dir)))
        self.assertEqual(read_file(self.index_path), read_file(test_index_path))

        images_dir = os.path.join(self.export_dir, 'images')
        post_image_dir = os.path.join(images_dir, 'ipynb2')
        self.assertEqual(['ipynb2'], os.listdir(images_dir))
        self.assertEqual(['image_1.png'], os.listdir(post_image_dir))
'''
    def test_md(self):
        md_path = resource_filename('blogger_cli',
                    'tests/tests_resources/md1.md')
        test_index_path = resource_filename('blogger_cli',
                    'tests/tests_resources/index/md_index.html')
        result = self.runner.invoke(cli, ['convert', '-b', 'test1',
                                md_path, '-v'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(['blog', 'images'],
                        os.listdir(self.export_dir))

        self.assertEqual(['index.html', 'md1.html', 'md1.md'],
                        os.listdir(self.blog_dir))
        self.assertEqual(read_file(self.index_path), read_file(test_index_path))


    def tearDown(self):
        tearDown(self)


if __name__ == '__main__':
    unittest.main()
