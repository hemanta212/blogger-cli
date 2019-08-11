import os
import unittest
from click.testing import CliRunner
from blogger_cli.cli import cli
from blogger_cli.tests.messages import BloggerMessage as BM


class TestBasic(unittest.TestCase):


    def setUp(self):
        self.runner = CliRunner()
        result = self.runner.invoke(cli, ['addblog', 'test1', '-s'])
        self.assertEqual(result.output, BM.addblog_success)
        self.assertEqual(result.exit_code, 0)


    def test_main(self):
        result = self.runner.invoke(cli)
        self.assertEqual(result.exit_code, 0)


    def test_addblog_existing(self):
        self.maxDiff = None
        result = self.runner.invoke(cli, ['addblog', 'test1'])
        self.assertEqual(result.output, BM.addblog_existing)
        self.assertEqual(result.exit_code, 0)


    def test_info_success(self):
        result = self.runner.invoke(cli, ['info'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, BM.info_success)
        result = self.runner.invoke(cli, ['info', '--all'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, BM.all_info_success)


    def test_setupblog_success(self):
        result = self.runner.invoke(cli, ['setupblog', 'test1'],
                                    input='\nn \nn \nn \nn \nn \nn \nn')
        self.assertEqual(result.exit_code, 0)


    def test_setdefault_success(self):
        result = self.runner.invoke(cli, ['setdefault', 'test1'])
        self.assertEqual(result.exit_code, 0)


    def test_config_success(self):
        result = self.runner.invoke(cli, ['config', '-b', 'test1',
                                    'working_dir', '~'])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(cli, ['config', '-b', 'test1', 'working_dir'])
        self.assertEqual(result.output, os.path.expanduser('~')+'\n')

        result = self.runner.invoke(cli, ['setdefault', 'test1'])
        result = self.runner.invoke(cli, ['config', 'blog_dir', '~/'])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(cli, ['config', 'blog_dir'])
        self.assertEqual(result.output, os.path.expanduser('~')+'\n')

        result = self.runner.invoke(cli, ['config', '-rm', 'default'])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(cli, ['config', '-b', 'test1', 'default'])
        self.assertEqual(result.exit_code, 0)



    def test_notadded(self):
        result = self.runner.invoke(cli, ['rmblog', 'test0'])
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(cli, ['setupblog', 'test0'])
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(cli, ['info', 'test0'])
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(cli, ['setdefault', 'test0'])
        self.assertEqual(result.exit_code, 0)


    def tearDown(self):
        result = self.runner.invoke(cli, ['rmblog', 'test1'])
        self.assertEqual(result.output, BM.rmblog_success)
        self.assertEqual(result.exit_code, 0)


if __name__ == '__main__':
    unittest.main()

