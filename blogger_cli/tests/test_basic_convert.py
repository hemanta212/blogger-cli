import os
import shutil
import unittest
from click.testing import CliRunner
from blogger_cli import ROOT_DIR
from blogger_cli.cli import cli
from pkg_resources import resource_filename


class TestBasic(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        HOME_DIR = os.path.expanduser("~")
        self.export_dir = os.path.join(HOME_DIR, ".blogger_tmp")
        os.mkdir(self.export_dir)
        self.blog_dir = os.path.join(self.export_dir, "blog")
        self.index_path = os.path.join(self.blog_dir, "index.html")
        self.runner.invoke(
            cli, ["addblog", "test1"], input=self.export_dir + "\nn \nn \nn \nn \nn \nn"
        )
        self.runner.invoke(cli, ["config", "-b", "test1", "blog_posts_dir", "blog/"])
        self.runner.invoke(cli, ["config", "-b", "test1", "blog_images_dir", "images/"])
        self.runner.invoke(cli, ["export", "-b", "test1", "blog_index", "-o", "blog"])

    def test_html(self):
        html_path = resource_filename("blogger_cli", "tests/tests_resources/html.html")
        test_index_path = resource_filename(
            "blogger_cli", "tests/tests_resources/index/html_index.html"
        )

        result = self.runner.invoke(cli, ["convert", "-b", "test1", html_path, "-v"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual({"blog", "images"}, set(os.listdir(self.export_dir)))

        self.assertEqual({"html.html", "index.html"}, set(os.listdir(self.blog_dir)))
        self.assertEqual(
            self.read_file(self.index_path), self.read_file(test_index_path)
        )

    @staticmethod
    def read_file(file_path):
        with open(file_path, "r", encoding="utf-8") as rf:
            data = rf.read()
            return data

    def test_ipynb(self):
        ipynb1_path = resource_filename(
            "blogger_cli", "tests/tests_resources/ipynb1.ipynb"
        )
        test_index_path = resource_filename(
            "blogger_cli", "tests/tests_resources/index/ipynb1_index.html"
        )

        result = self.runner.invoke(cli, ["convert", "-b", "test1", ipynb1_path, "-v"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual({"blog", "images"}, set(os.listdir(self.export_dir)))

        self.assertEqual(
            {"index.html", "ipynb1.html", "ipynb1.ipynb"},
            set(os.listdir(self.blog_dir)),
        )
        self.assertEqual(
            self.read_file(self.index_path), self.read_file(test_index_path)
        )

    def test_ipynb_images_and_index(self):
        self.test_ipynb()
        ipynb2_path = resource_filename(
            "blogger_cli", "tests/tests_resources/ipynb2.ipynb"
        )
        test_index_path = resource_filename(
            "blogger_cli", "tests/tests_resources/index/ipynb2_index.html"
        )

        result = self.runner.invoke(cli, ["setdefault", "test1"])
        result = self.runner.invoke(cli, ["convert", ipynb2_path, "-v"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual({"blog", "images"}, set(os.listdir(self.export_dir)))

        self.assertEqual(
            {
                "index.html",
                "ipynb1.html",
                "ipynb1.ipynb",
                "ipynb2.html",
                "ipynb2.ipynb",
            },
            set(os.listdir(self.blog_dir)),
        )
        self.assertEqual(
            self.read_file(self.index_path), self.read_file(test_index_path)
        )

        images_dir = os.path.join(self.export_dir, "images")
        post_image_dir = os.path.join(images_dir, "ipynb2")
        self.assertEqual(["ipynb2"], os.listdir(images_dir))
        self.assertEqual(["image_1.png"], os.listdir(post_image_dir))

    def test_md(self):
        md_path = resource_filename("blogger_cli", "tests/tests_resources/md1.md")
        test_index_path = resource_filename(
            "blogger_cli", "tests/tests_resources/index/md_index.html"
        )

        result = self.runner.invoke(cli, ["convert", "-b", "test1", md_path, "-v"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual({"blog", "images"}, set(os.listdir(self.export_dir)))

        self.assertEqual(
            {"index.html", "md1.html", "md1.md"}, set(os.listdir(self.blog_dir))
        )
        self.assertEqual(
            self.read_file(self.index_path), self.read_file(test_index_path)
        )

    def test_md_meta_and_custom_templates(self):
        md_path = resource_filename("blogger_cli", "tests/tests_resources/md2.md")
        test_results_path = resource_filename(
            "blogger_cli", "tests/tests_resources/results/md2.html"
        )

        test_index_path = resource_filename(
            "blogger_cli", "tests/tests_resources/index/meta_and_templates_index.html"
        )

        templates_path = os.path.join(
            ROOT_DIR, "tests", "tests_resources", "_blogger_templates"
        )

        result = self.runner.invoke(
            cli, ["convert", "-b", "test1", md_path, "-v", "-temp", templates_path]
        )
        self.assertEqual(result.exit_code, 0)
        self.assertEqual({"blog", "images"}, set(os.listdir(self.export_dir)))
        topic_dir = os.path.join(self.blog_dir, "meta")
        self.assertEqual({"md2.html", "md2.md"}, set(os.listdir(topic_dir)))
        converted_html = os.path.join(topic_dir, "md2.html")

        self.assertEqual(
            self.read_file(self.index_path), self.read_file(test_index_path)
        )
        # os.system('cp '+ converted_html + ' ' + test_results_path)
        self.assertEqual(
            self.read_file(converted_html), self.read_file(test_results_path)
        )

    def tearDown(self):
        self.runner.invoke(cli, ["rmblog", "test1"])
        shutil.rmtree(self.export_dir)


if __name__ == "__main__":
    unittest.main()
