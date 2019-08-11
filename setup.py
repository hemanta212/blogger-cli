from setuptools import setup

setup(
    name='blogger-cli',
    version = "1.1.0",
    description = "Blogger cli is a CLI tool to convert ipynb, md, html file to responsive html files.",
    authors = ["hemanta212 <sharmahemanta.212@gmail.com>"],
    readme = 'README.md',
    repository = "https://github.com/hemanta212/blogger-cli",
    documentation = "https://hemanta212.github.io/blogger-cli",
    keywords = ["jupyter notebook", "github pages", "blogger"],
    license = "MIT",
    packages=['blogger_cli', 'blogger_cli.commands', 'blogger_cli.cli_utils',
                'blogger_cli.blog_manager', 'blogger_cli.converter'],
    include_package_data=True,
    install_requires=[
        'click', 'nbconvert', 'markdown', 'bs4'
    ],
    entry_points='''
        [console_scripts]
        blogger=blogger_cli.cli:cli
    ''',
)
