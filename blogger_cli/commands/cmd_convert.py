import click
import os
from blogger_cli.converter import ipynb_to_html
from blogger_cli.cli import pass_context


def start():
    #file_path = os.path.abspath(os.path.expanduser(input('file dir')))
    file_dir = 'ipynb_test'
    os.chdir(file_dir)
    for f in os.listdir():
        try:
            file_list = f.split(".")
            if "ipynb" in file_list:
                print("found", f)
                ipynb_to_html.generate_html(f)
        except:
            continue



@click.command('convert', short_help='Convert files to html')
@pass_context
def cli(ctx):
    """Convert diffrent file format to html"""
    ctx.log("convert is not called")
    start()
