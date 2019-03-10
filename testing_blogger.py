import unittest
from click.testing import CliRunner
import blogger

class TestBlogger(unittest.TestCase):
    def test_main(self):
        runner = CliRunner()

        result = runner.invoke(blogger.main, ['hi'])
        self.assertEqual(result.exit_code,0)

        result = runner.invoke(blogger.main)
        self.assertEqual(result.exit_code,0)


    def test_blogs(self):
        runner = CliRunner()

        result = runner.invoke(blogger.blogs)
        self.assertEqual(result.exit_code,0)
        message = 'No option provided\n'
        self.assertEqual(result.output, message)

        result = runner.invoke(blogger.blogs, ['-a'])
        self.assertEqual(result.exit_code,2)
        message = 'Error: -a option requires an argument\n'
        self.assertEqual(result.output, message)

        result = runner.invoke(blogger.blogs, ['-a', 'testapp1'],
                               input='n')
        message = [
            'no blog registered yet',
            'registering..',
            "Setup this blog's configs now? [y/N]: n",
            "Registered testapp1 succesfully\n",
        ]
        self.assertEqual(result.output, "\n".join(message))
        self.assertEqual(result.exit_code,0)


        result = runner.invoke(blogger.blogs, ['-a', 'testapp'],
                               input='n')
        message = [
            'testapp not registered yet',
            'registering..',
            "Setup this blog's configs now? [y/N]: n",
            "Registered testapp succesfully\n",
        ]
        self.assertEqual(result.output, "\n".join(message))
        self.assertEqual(result.exit_code,0)

        result = runner.invoke(blogger.blogs, ['-a', 'testapp'])
        self.assertEqual(result.exit_code,0)
        message="blog already exists\n"
        self.assertEqual(result.output, message)

        result = runner.invoke(blogger.blogs, ['-def', 'testapp'])
        self.assertEqual(result.exit_code,0)
        message="Default blog set to testapp\n"
        self.assertEqual(result.output, message)

        result = runner.invoke(blogger.blogs, ['-def', 'testa'])
        self.assertEqual(result.exit_code,0)
        message="testa not registered yet\n"
        self.assertEqual(result.output, message)

        result = runner.invoke(blogger.blogs, ['-rm', 'testapp'])
        self.assertEqual(result.exit_code,0)
        message = 'removing..\nDeleted testapp\n'
        self.assertEqual(result.output, message)

        result = runner.invoke(blogger.blogs, ['config'])
        self.assertEqual(result.exit_code,0)

        result = runner.invoke(blogger.blogs, ['config_file'])
        self.assertEqual(result.exit_code,0)

        result = runner.invoke(blogger.blogs, ['list'])
        self.assertEqual(result.exit_code,0)

        result = runner.invoke(blogger.blogs, ['randomkey'])
        self.assertEqual(result.exit_code,0)
        message = ["unsupported info argument: use one of",
                        "[list, config, config_file]\n"]
        self.assertEqual(result.output, "\n".join(message))


    def test_convert(self):
        runner = CliRunner()

#        result = runner.invoke(blogger.convert, ['txt', '~/Khabar-board/'])
#        self.assertEqual(result.exit_code,0)
#        message = 'txt\n'
#        self.assertEqual(result.output, message)

        result = runner.invoke(blogger.convert, ['html', '/raju/hirani/'])
        self.assertEqual(result.exit_code,0)
        message = 'Please enter a valid file/folder path\nNone\n'
        self.assertEqual(result.output, message)

        result = runner.invoke(blogger.convert, ['/raju/hirani/'])
        self.assertEqual(result.exit_code,0)
        message = 'Please enter a valid file/folder path\nNone\n'
        self.assertEqual(result.output, message)

 #       result = runner.invoke(blogger.convert, ['~/Khabar-board/'])
#       self.assertEqual(result.exit_code,0)
#        message = 'please give file_type to convert from\nNone\n'
#        self.assertEqual(result.output, message)

    def test_config(self):
        runner = CliRunner()
        result = runner.invoke(blogger.config, ['keys'])
        self.assertEqual(result.exit_code,0)

        result = runner.invoke(blogger.config, ['config'])
        self.assertEqual(result.exit_code,0)

        result = runner.invoke(blogger.config, ['html_dir', '/test/path/'])
        self.assertEqual(result.exit_code,0)
        message=["checking for default blog",
                 "No default blog set! Set one using",
                 "blogger-cli blogs -def <blog_name>\n",
                ]
        self.assertEqual(result.output, "\n".join(message))

        runner.invoke(blogger.main, ['blogs', '-a', 'testapp'], input='n')
        result = runner.invoke(blogger.main, ['blogs', '-def', 'testapp'])
        self.assertEqual(result.exit_code,0)
        message = "Default blog set to testapp\n"
        self.assertEqual(result.output, message)

        result = runner.invoke(blogger.config, ['html_dir', '/test/path/'])
        self.assertEqual(result.exit_code,0)
        message=["checking for default blog",
                 "using testapp as default",
                 "added /test/path/ to html_dir\n"
                ]
        self.assertEqual(result.output, "\n".join(message))

        result = runner.invoke(blogger.config, ['html-dir', '/test/path/'])
        self.assertEqual(result.exit_code,0)
        message=["checking for default blog",
                 "using testapp as default",
                 "Invalid config key 'html-dir'\n"
                ]
        self.assertEqual(result.output, "\n".join(message))

        result = runner.invoke(blogger.config, ['htmldir'])
        self.assertEqual(result.exit_code,0)
        message=["checking for default blog",
                 "using testapp as default",
                 "Invalid config key 'htmldir'\n"
                ]
        self.assertEqual(result.output, "\n".join(message))

        result = runner.invoke(blogger.config, ['html_dir'])
        self.assertEqual(result.exit_code,0)
        message=["checking for default blog",
                 "using testapp as default",
                 "html_dir: /test/path/\n"
                ]
        self.assertEqual(result.output, "\n".join(message))

        result = runner.invoke(blogger.config, ['delete'], input='n')
        self.assertEqual(result.exit_code,1)
        message = 'delete the config file? [y/N]: n\nAborted!\n'
        self.assertEqual(result.output, message)

        result = runner.invoke(blogger.config, ['delete'], input='y')
        self.assertEqual(result.exit_code,0)
        message = 'delete the config file? [y/N]: y\ndeleted config file\n'
        self.assertEqual(result.output, message)


if __name__ == '__main__':
    unittest.main()
