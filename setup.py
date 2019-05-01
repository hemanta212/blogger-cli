from setuptools import setup

setup(
    name='blogger-cli',
    version='0.0.1',
    packages=['blogger_cli', 'blogger_cli.commands',
              'blogger_cli.cli_utils', 'blogger_cli.converter'],
    include_package_data=True,
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        blogger=blogger_cli.cli:cli
    ''',
)
