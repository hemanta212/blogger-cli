# -*- coding: utf-8 -*-
"""
Backup setup.py for install
"""

import codecs
from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with codecs.open(path.join(here, "README.md"), "r", "utf-8") as f:
    readme = f.read()

packages = [
    "blogger_cli",
    "blogger_cli.blog_manager",
    "blogger_cli.cli_utils",
    "blogger_cli.commands",
    "blogger_cli.commands.convert_utils",
    "blogger_cli.commands.export_utils",
    "blogger_cli.commands.feed_utils",
    "blogger_cli.commands.serve_utils",
    "blogger_cli.converter",
    "blogger_cli.resources",
    "blogger_cli.tests",
]

package_data = {
    "": ["*"],
    "blogger_cli.resources": [
        "blog_layout/*",
        "blog_layout/_blogger_templates/*",
        "blog_layout/assets/css/*",
        "blog_layout/blog/*",
    ],
    "blogger_cli.tests": [
        "tests_resources/*",
        "tests_resources/_blogger_templates/*",
        "tests_resources/index/*",
        "tests_resources/results/*",
    ],
}

install_requires = [
    "bs4>=0.0.1,<0.0.2",
    "click>=7.0,<8.0",
    "colorama>=0.4.1,<0.5.0",
    "feedgen>=0.9.0,<0.10.0",
    "markdown>=3.1,<4.0",
    "misspellings>=1.5,<2.0",
    "nbconvert>=5.5,<6.0",
    "pyspellchecker>=0.5.0,<0.6.0",
    "selectolax>=0.2.1,<0.3.0",
]

entry_points = {
    "console_scripts": ["blogger = blogger_cli.cli:cli"],
}


setup(
    name="blogger-cli",
    version="1.2.4",
    description="Blogger cli is a CLI tool to convert ipynb, md, html file to responsive html files.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="hemanta212",
    author_email="sharmahemanta.212@gmail.com",
    url="https://hemanta212.github.io/blogger-cli",
    keywords=["jupyter notebook", "github pages", "blogger"],
    license="MIT",
    packages=packages,
    package_data=package_data,
    include_package_data=True,
    install_requires=install_requires,
    entry_points=entry_points,
    python_requires=">=3.5,<4.0",
    project_urls={
        "Bug Reports": "https://github.com/hemanta212/blogger-cli/issues",
        "Source": "https://github.com/hemanta212/blogger-cli/",
    },
)
