'''
Config manager file to quickly write app configurations
'''
import json
import datetime
import os
from logger_file import Logger

logger = Logger(console=False).get_logger()


class Config:
    '''
    Config class with methods
        write(key, value)
        read() #reads value of a key
        get_dict(value)#gives a key from value
        delete_key(key)#deletes a key
        delete_config()#deletes a config file
        empty_config()#empties a config file
    '''

    def __init__(self, file, backup_dir='~/.cli_backup/'):
        self.file_path = os.path.expanduser(file)
        self.file = os.path.basename(file)
        self.backup_dir = os.path.expanduser(backup_dir)

    def __str__(self):
        return self.file_path

    def __repr__(self):
        return "file: {0}, backup_dir: {1}".format(self.file, self.backup_dir)

    def write(self, key, value):
        '''
        writes to a config file as a dictionary

        params:
            key:name of setting
            value: value of setting
        Usage:
            Config.write('user.email','a@a.com')
         '''
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w'):
                logger.debug("file created")

        with open(self.file_path, 'r')as rf:
            content = rf.read()

            if content != "":
                logger.debug("file not empty, appending..")
                read_dict = json.loads(content)
                read_dict[key] = value
                self.write_dict(read_dict)
            else:
                logger.debug("file empty, first entry")
                dump_dict = {}
                dump_dict[key] = value
                self.write_dict(dump_dict)

    def write_dict(self, new_dict):
        '''
        params: dictionary containing configs
        returns : nothing
        '''
        with open(self.file_path, 'w')as rf:
            json.dump(new_dict, rf)
            logger.debug("succesfully added config dict")

    def delete_config(self, backup=True):
        '''
        Deletes config_file to backup_dir (both specified in Config class)
        Params:
            backup [boolean] : Defaults to True
        '''
        # manage name acc to current datetime
        name = str(datetime.datetime.now()) + '.cfg'
        if backup:
            if not os.path.exists(self.backup_dir):
                os.makedirs(self.backup_dir)
                logger.debug('creating backup dir')

            if os.path.exists(self.file_path):
                new_name = os.path.join(self.backup_dir, name)
                os.rename(self.file_path, new_name)
                logger.debug('deleted')

            else:
                logger.debug("file not found, check if it exists")
        else:
            os.remove(self.file_path)
            logger.debug('deleted permanently')

    def file_exists(self):
        '''returns True or False '''
        if os.path.exists(self.file_path):
            return True
        else:
            return False

    def get_dict(self):
        '''
        returns: A python dictionary of all configs
        '''
        with open(self.file_path, 'r')as rf:
            json_data = rf.read()
            try:
                content = json.loads(json_data)
                return content
            except Exception as e:
                raise e  # ("file maybe empty or not contain json data")

    def read(self, key=None, value=None, all_keys=False, all_values=False):
        '''
            Reads and return key or value from config file
                (returns config dict if no parameter)
            Params:
               [o] key: Key of dictionary to get the value of
               [o] value : value of dictionary to get key of
               [o] all_keys [bool] : True returns all keys dict object
               [o] all_values [bool]: True returns all values dict obj.
        '''
        # Check if more than 1 kwargs given
        arguments = (key, value, all_keys, all_values)
        given = [1 for i in arguments if i]
        if len(given) >= 2:
            raise ValueError("More than 1 arguments given")

        # ensure the file exists.
        self.file_exists()
        # load the dictionary from config
        configs = self.get_dict()
        if all_keys:
            return configs.keys()

        elif all_values:
            return configs.values()

        elif key:
            return configs.get(key)

        elif value:
            key = [k for k, v in configs.items() if v == value]
            if len(key) == 1:
                return key[0]
            elif len(key) > 1:
                return key
            else:
                raise KeyError("The value doesnot exist in config")
        else:
            return self.get_dict()

    def init_config(self):
        '''Empties the file
        Raises error with .read() method but applicable with write()
        '''

        with open(self.file_path, 'w'):
            logger.debug("file emptied")

    def delete_key(self, key):
        '''
         Deletes a given key from the config
        '''
        config_dict = self.get_dict()
        del config_dict[key]
        self.write_dict(config_dict)
