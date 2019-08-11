'''
                                        Tests only export command.
                            THE TESTS RUN IN ALPHABETICAL ORDER OF NAME OF FUNCTION
                            |except for setUP (runs first) and tearDown (run last)|
'''

import os
import shutil
import unittest
from click.testing import CliRunner
from blogger_cli.cli import cli
from blogger_cli.tests.messages import BloggerMessage as BM


class TestBasic(unittest.TestCase):


    def setUp(self):
        self.runner = CliRunner()
        self.export_dir = os.path.expanduser('~/.blogger_tmp/')
        if not os.path.exists(self.export_dir):
            os.mkdir(self.export_dir)
        self.runner.invoke(cli, ['addblog', 'test1'],
                    input=self.export_dir + '\nn \nn \nn \nn \nn \nn')


    def test_blog_config(self):
        result = self.runner.invoke(cli, ['export','-b', 'test1', 'blog_config'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(['test1.json'], os.listdir(self.export_dir))

        result = self.runner.invoke(cli, ['setdefault', 'test1'])
        result = self.runner.invoke(cli, ['export', 'blog_config',
                                    '-o', self.export_dir])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(['test1.json'], os.listdir(self.export_dir))

        self.runner.invoke(cli, ['config', '-rm', 'default'])


    def test_blog_index(self):
        result = self.runner.invoke(cli, ['export','-b', 'test1', 'blog_index'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(['index.html'], os.listdir(self.export_dir))


        self.runner.invoke(cli, ['setdefault', 'test1'])
        result = self.runner.invoke(cli, ['export', 'blog_index',
                                    '-o', 'blog'])
        self.assertEqual(result.exit_code, 0)
        blog_dir = os.path.join(self.export_dir, 'blog')
        self.assertEqual(['index.html'], os.listdir(blog_dir))

        self.runner.invoke(cli, ['config', '-rm', 'default'])



    def test_design_assets(self):
        result = self.runner.invoke(cli, ['export','-b', 'test1', 'design_assets'])
        self.assertEqual(result.exit_code, 0)
        expected_files = {'css'}
        self.assertEqual(expected_files,
                         set(os.listdir(self.export_dir)))

        result = self.runner.invoke(cli, ['setdefault', 'test1'])
        result = self.runner.invoke(cli, ['export', 'design_assets',
                                    '-o', 'assets'])
        self.assertEqual(result.exit_code, 0)
        assets_dir = os.path.join(self.export_dir, 'assets')
        self.assertEqual(expected_files, set(os.listdir(assets_dir)))

        self.runner.invoke(cli, ['config', '-rm', 'default'])


    def test_export_blog_layout(self):
        assets_dir = os.path.join(self.export_dir, 'assets')

        result = self.runner.invoke(cli, ['setdefault', 'test1'])
        result = self.runner.invoke(cli, ['export', 'blog_layout',
                                    '-o', 'assets'])
        self.assertEqual(result.exit_code, 0)
        expected_files = {'assets', 'blog', 'index.html',
                        '_blogger_templates', 'images'}
        self.assertEqual(expected_files, set(os.listdir(assets_dir)))

        self.runner.invoke(cli, ['config', '-rm', 'default'])
        shutil.rmtree(self.export_dir)


    def test_export_blog_template(self):
        assets_dir = os.path.join(self.export_dir, 'assets')

        result = self.runner.invoke(cli, ['setdefault', 'test1'])
        result = self.runner.invoke(cli, ['export', 'blog_template',
                                    '-o', 'assets'])
        self.assertEqual(result.exit_code, 0)
        expected_files = {'css.html', 'dark_theme.html','navbar_data.html',
                        'disqus.html', 'google_analytics.html', 'js.html',
                        'layout.html', 'li_tag.html', 'light_theme.html',
                        'mathjax.html', 'navbar.html'}
        self.assertEqual(expected_files, set(os.listdir(assets_dir)))
        self.runner.invoke(cli, ['config', '-rm', 'default'])
        shutil.rmtree(self.export_dir)


    def tearDown(self):
        self.runner.invoke(cli, ['rmblog', 'test1'])
        try:
            shutil.rmtree(self.export_dir)
        except FileNotFoundError:
            #folder already deleted by export_blog_template
            pass


if __name__ == '__main__':
    unittest.main()
