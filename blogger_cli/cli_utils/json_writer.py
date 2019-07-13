'''
Config manager file to quickly write app configurations
'''
import json
import datetime
import os

class Config:
    '''
    Config class with methods
        write(key, value):
            eg Config.write('parent:child:sub_child', 'value')
            Config.write('key','value')
        read(key=None, value=None, all_keys=False, all_values=False)
        get_dict(): gives you config dict
        delete_key(key): deletes a key
        delete_file(backup=True): deletes the config file
    '''

    def __init__(self, file, backup_dir='~/.cli_backup/'):
        self.file_path = os.path.abspath(os.path.expanduser(file))
        self.file = os.path.basename(self.file_path)
        self.file_dir = os.path.dirname(self.file_path)
        self.backup_dir = os.path.abspath(os.path.expanduser(backup_dir))
        # check if file exists and json readable otherwise create one
        self.handle_file()

    def __str__(self):
        return self.file_path

    def __repr__(self):
        return "file: {0}, backup_dir: {1}".format(
            self.file_path, self.backup_dir)

    def handle_file(self):
        file_exists = os.path.exists(self.file_path)
        folder_exists = os.path.exists(self.file_dir)
        if file_exists:
            try:
                self.get_dict()
            except (Exception, ValueError):
                file_exists = False
        if not file_exists:
            if not folder_exists:
                os.makedirs(self.file_dir)
            self.write_dict({})

    def get_dict(self):
        '''
        Gives you the whole config dictionary from config file
        '''
        with open(self.file_path, 'r')as rf:
            data = json.load(rf)
            return data

    def write_dict(self, new_dict):
        '''
        params: dictionary containing configs
        returns : nothing
        '''
        with open(self.file_path, 'w')as rf:
            json.dump(new_dict, rf, indent=2)

    def __dict_accesor(self, dict_name, key_list):
        '''
        Makes multi level dict easy to access name['a']['b']['c']......

        Params:
            dict_name(str) = name of dictionary
            key_list(list) = list of keys to use as ['key1']['key2']....
        Returns:
            A string like name['k1']['k2'] Maybe use it with exec/eval
        '''
        for i in key_list:
            dict_name += "['{0}']".format(i)
        return dict_name

    def write(self, key, value):
        '''
        writes to a config file as a dictionary

        params:
            key:name of setting, path of setting
            value: value of setting
        Usage:
            Config.write('user.email','a@a.com')
            Config.write('
         '''

        def make_depth(key_list):
            '''
            Creates depth assuming nothing existed before
            Returns:
                 A dictionary with all list items in nested form and last
                 item being assigned the given value
            '''
            value = None
            key_list.reverse()
            for key in key_list:
                value = {key: value}
            return value

        def ensure_path(key_list, data_dict):
            first_half = ''
            second_half = ' = temp_dict'
            temp_dict = data_dict

            for index, item in enumerate(key_list):
                if item in temp_dict:
                    temp_dict = temp_dict[item]
                else:
                    temp_dict.update(
                        make_depth(key_list[index:])
                    )
                    first_half = self.__dict_accesor(
                        'data_dict', key_list[:index]
                    )
                    exec(first_half + second_half)
                    break

        with open(self.file_path, 'r')as rf:
            data_dict = json.load(rf)
            key_list = [ i.strip() for i in key.split(":") ]
            first_half = self.__dict_accesor('data_dict', key_list)
            second_half = '= value'
            ensure_path(key_list, data_dict)
            exec(first_half + second_half)

            self.write_dict(data_dict)

    def read(self, key=None, value=None, all_keys=False, all_values=False):
        '''
            Reads and return key or value from config file
                (returns config dict if no parameter)
            Params:
               [o] key: key of dict. Use (:) eg: key:nkey for depth
               [o] value : value of dictionary to get key of
               [o] all_keys [bool] : True returns all keys dict object
               [o] all_values [bool]: True returns all values dict obj.
        '''
        # Check if more than 1 kwargs given
        arguments = (key, value, all_keys, all_values)
        given = [1 for i in arguments if i]
        if len(given) >= 2:
            raise ValueError("More than 1 arguments given")
        # load the dictionary from config
        configs = self.get_dict()
        if all_keys:
            return list(configs.keys())

        elif all_values:
            return list(configs.values())

        elif key:
            cfg_dict = configs
            key_list = key.split(':')
            for i in key_list:
                key = i.strip()
                cfg_dict = cfg_dict.get(key)
                if not cfg_dict:
                    return None
            return cfg_dict

        elif value:
            key = [k for k, v in configs.items() if v == value]
            if len(key) == 1:
                return key[0]
            return key

    def delete_key(self, key):
        '''
         Deletes a given key from the config
        '''
        key_list = key.split(':')
        config_dict = self.get_dict()
        dict_accesor = self.__dict_accesor('config_dict', key_list)
        exec('del ' + dict_accesor)
        self.write_dict(config_dict)

    def delete_file(self, backup=True):
        '''
        Deletes config_file to backup_dir (both specified in Config class)
        Params:
            backup [boolean] : Defaults to True
        '''
        # manage name acc to current datetime
        date_today = datetime.datetime.now()
        str_format = '%d_%b_%Y_%H_%M_%S'
        name = date_today.strftime(str_format) + '.cfg'

        if backup:
            if not os.path.exists(self.backup_dir):
                os.makedirs(self.backup_dir)

            new_name = os.path.join(self.backup_dir, name)
            os.rename(self.file_path, new_name)

        else:
            os.remove(self.file_path)
