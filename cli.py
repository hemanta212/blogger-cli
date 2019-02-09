''' Command line tool to convert ipynb files to html and manage them '''
__Author__ = "Hemanta Sharma"

import os
from converter import convert
import sys

class setup:
    '''Save user preference in the first run.
    Contains:
        ipynb_path
        gen_rel_path
        write_config
         '''

    def __init__(self):
        '''Initializes setup for first time use
        '''
        pass

    def ipynb_path(self):
        ''' Takes input from user for default path to look for ipynb files
        default = None, Nullable = True '''
        path = input("Default jupyter folder []")


    def gen_rel_path(self, path):
        '''Generate path relative to the userprofile path (home of user)

        params= str of path
        returns = generated full str of path
        eg: gen_rel_path("/app/config/tools/")
        '''
        user_path = os.environ.get("USERPROFILE")
        full_path = os.path.join(user_path, path)
        req_path = os.path.normpath(full_path)
        if not os.path.exists(req_path):
            os.mkdirs(req_path)
        return req_path

    def write_config(self, dose):
        '''writes a given line dict to config.json of the app
        params = dictionary
        eg: write_config({"ipynb_dir":"C:/users/user/htmlconvert/"}
        '''
        config_path = gen_rel_path('/htmlconvert/')
        with open(f'{config_path}/config.json', 'w') as rf:
            if rf.read() is not None:
                data = json.load(rf)
                data.append()





