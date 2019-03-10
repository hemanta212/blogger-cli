import os

def type_or_path(given):
    dots = given.find('.') 
    f_slash = given.find('/')
    b_slash = given.find('\\')

    #if the mactching fails -1 is returned so if all are equal, it means
    #all are -1 and every matching has failed so 'given' is not path 
    if dots == f_slash == b_slash:
        type, path = given, None  

    else:
        type, path = None, given

    return type, path

def get_from(orig_type, orig_path):
    '''Checks if folders' files are acc to orig (if given)
    else process the folder to retrieve orig ext intelligently
    Params:
        orig_path = name or path of folder/file
        orig [def=None] = original ext type given by user
    '''
    
    #check if user has omitted orig_type and only typed orig_path as click 
    #still interprets as orig_type cause its the first argument passed.
    if orig_type and not orig_path:
        orig_type, orig_path = type_or_path(orig_type)

    #support ~/ use 
    if orig_path:
        orig_path = os.path.expanduser(orig_path)

    if orig_path and os.path.isdir(orig_path):

        for dirpath, folders, filename in os.walk(orig_path):
            ext_list = [os.path.splitext(i)[-1] for i in filename]

            if orig_type and '.' + orig_type not in ext_list:
                print('Your given file_type not present in folder')

            elif orig_type and '.'+ orig_type in ext_list:
                return orig_type 

            elif not orig_type:
                if ext_list and ext_list.count(ext_list[0]) == len(ext_list):
                    sample_file_ext = ext_list[0]
                    orig_type = sample_file_ext[1:]
                    return orig_type

                else:
                    print("please give file_type to convert from")
            break;

    elif orig_path and  os.path.isfile(orig_path):
        file = os.path.basename(orig_path) 
        ext = os.path.splitext(file)[-1]
        print(ext[1:])
        return ext[1:]

    elif orig_path:
        print("Please enter a valid file/folder path")

    else:#no orig_path given use user config to get default path
        return 'use_config'

