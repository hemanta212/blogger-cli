'''
Blogger-cli project main file for handling CLI.
'''
__author__ = "Hemanta Sharma (hemanta212 github)"
__version__ ='0.1.0'

import os
from pprint import pprint
import click
import jmespath
from config_writer import Config as Cfg
from logger_file import Logger
from cli_utils.blog import Blog
from cli_utils import converter as Converter

cfg = Cfg('~/.blogger_cli.cfg', backup_dir='~/.blogger_cli/backup/')
logger_cls = Logger(level='debug', console=False)
logger = logger_cls.get_logger()


@click.group()
def main():
    '''
     A testing project for blogger-cli project
    '''


@main.command()
def hi():
    '''
    A comand test if succesfully installed
    '''
    message = '''
            WELCOME TO BLOGGER_CLI
Blogger cli is succesfully installed and working!

use blogger-cli --help for more info!
    '''
    print(message)


@main.command()
@click.option('--blog', '-b', help='name of the blog')
@click.argument('command', nargs=-1, required=False)
def config(command, blog):

    try:
        cfg.get_dict()

    except FileNotFoundError:
        message = ["Config uninitialized!",
                    "Use blogger-cli blogs -a <name>",
                    "to initialize it.",
            ]
        print(" ".join(message))
        return 0


    if not command and not blog:
        print("Configuration file:", cfg)
        pprint(cfg.get_dict())

    elif command and command[0] == 'delete':
         if click.confirm('delete the config file?', abort=True):
            cfg.delete_config()
            print('deleted config file')

    else:
        if not blog:
            click.secho("checking for default blog")
            default_blog = jmespath.search('default', cfg.get_dict())
            if default_blog:
                blog = default_blog
                print("using",blog,"as default")
                blog_obj = Blog(cfg, blog)
            else:
                message = ["No default blog set! Set one using",
                            "blogger-cli blogs -def <blog_name>",
                          ]
                print("\n".join(message))
                return 0

        else: #if blog is given 
            blog_obj = Blog(cfg, blog)

        if blog_obj.exists():
            if not command:
                blog_dict = blog_obj.get_dict()
                [print(k+":",v) for k,v in blog_dict.items()]

            elif len(command) == 1:
                if command[0] == 'keys':
                    blog_dict = blog_obj.get_dict()
                    [print(k) for k,v in blog_dict.items()]

                else:
                    (key,) = command 
                    try:
                        value = blog_obj.get_value(key)
                        print(key+":", value)
                    except KeyError:
                        print("Invalid config key", '\'' + key + '\'')
            else:
                key, value = command
                blog_attr = cfg.read(key=blog)
                if key in blog_attr:
                    blog_obj.add_key(key, value)
                    print("added", value, "to", key)
                else:
                    print("Invalid config key", '\'' + key + '\'')


@main.command()
@click.option('--setup', '-s', help="setup all config values for a blog")
@click.option('--default', '-def', help='name of default blog to use')
@click.option('--remove', '-rm', help="remove a blog")
@click.option('--add', '-a', help="add a new blog")
@click.argument('info', required=False)
def blogs(setup, add, remove, info, default):
    '''
    Manages blogs setting, adding, removing and listing all blogs.
    '''

    if add:
        # the value of add is a blog name. same other params
        blog_name = add
        blog_obj = Blog(cfg, blog_name)
        if not blog_obj.exists():
            blog_obj.register()
            if click.confirm("Setup this blog's configs now?"):
                setup = blog_name
            else:
                print("Registered", blog_name, "succesfully")
                return 0
        else:
            click.secho("blog already exists")
            return 0

    if setup:
        blog_name = setup
        blog_obj = Blog(cfg, blog_name)

        if blog_obj.exists():
            click.secho("Running a config setup for {0}".format(blog_name))
            blog_attr = cfg.read(key=blog_name)
            for k, v in blog_attr.items():
                value = click.prompt(k+'[n to skip]', default=v)
                if value != 'n':
                    blog_obj.add_key(k, value)
            click.secho("successfully updated configs")

    elif default:
        blog_name = default
        blog_obj = Blog(cfg, blog_name)
        if blog_obj.exists():
            blog_obj.set_default(blog_name)
            print("Default blog set to",blog_name)
    
    elif remove:
        blog_name = remove
        blog_obj = Blog(cfg, blog_name)
        if not blog_obj.exists():
            print(blog_name, "doesnot exists")
        else:
            click.secho("removing..")
            blog_obj.delete()
            click.secho("Deleted {0}".format(blog_name))

    elif info:
        config_file = cfg.__str__()

        if info == 'config_file':
            print(cfg)
            return 0

        if not os.path.isfile(config_file):
            print("Initialize the file with blogger-cli blogs -a <name> first")
            return 0

        elif info == 'list':
            [print(i) for i in Blog.blogs(cfg)]

        elif info == 'config':
            pprint(cfg.get_dict())

        else:
            message = ["unsupported info argument: use one of",
                        "[list, config, config_file]",]
            print("\n".join(message))

    else:
        click.secho("No option provided")

@main.command()
@click.argument('orig_type', required=False)
@click.argument('orig_path', type=click.Path(), required=False)
@click.argument('dest_type', required=False)
@click.argument('dest_path',type=click.Path(),required=False)
@click.option('--blog','-b', help="name of blog whose config to use when needed")
def convert(orig_type, orig_path, dest_type, dest_path, blog):
    supported_conversions = {'ipynb':'html'}
    from_ = Converter.get_from(orig_type, orig_path)
    print(from_)

if __name__ == "__main__":
    main()
