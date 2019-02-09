import os
import datetime 

os.chdir("/storage/emulated/0/console_editor/")

#utilities or menus
def filemaker(filename, content =""):
    with open(filename, "w") as f:
        f.write(content)

def file_exists(filename):
    files_list = os.listdir()
    return True if filename in files_list else False
    

#Actural scripts/////
def welcome():
    print("welcome to the console text-editor version 1.0")
    print("NEW | OLD | RENAME | HELP")
    try:
        user_input = input().lower().strip().split(" ")
    except:
        user_input ==  ""    
    if user_input[0] == "new" or "":
        if user_input == "new":
            try:
                input_filename = user_input[1]
                create(input_filename)
            except:
                print("Invalid syntax, read help if you dunno it")    
                welcome()
        else:
            create("")    
    elif user_input[0] == "rename":
        try:
            old_name = user_input [1].strip()
            new_name = user_input [2].strip()
            
            if file_exists(old_name):#look in utilities
                os.rename(old_name, new_name)
            else:
                print("file does not exist")
                welcome()
        except:
            print("Type rename, then old file and new name")        
                
    elif user_input[0] == "old":
        try:
            old_name = user_input[1].strip()
            if file_exists(old_name):
                with open(old_name, "r+") as fr:
                    print(fr.read())
                    print("Write from here,, It will get appended at the end")
                    content = input()
                    fr.write(content)
        except:
            print("invalid syntax, use help if needed!")                 
            
            
            
            
def create(input_filename):
    if input_filename == "":
        name = str(datetime.date.today())
        filename = name + ".txt"
        filemaker(filename)#look in utilities part
        write(filename)
    else:
        name, ext = os.path.splitext(input_filename)
        if ext != "":
            filename = name + ext
            filemaker(filename)
            write(filename,choice="choice")
        else:
            print("please give filename with ext like .txt, .py or just hit enter only to write default txt file")
            return create()

def writefile(filename, choice="default"):
    print("start writeing ")
    content = input()
    filemaker(filename,content)
    
    content = content.strip()
    if content != "" and choice == "default":
        name, ext = os.path.splitext(filename)
        new_name = content.split(" ", 1)[0]
        new_filename = new_name + ext
        os.rename(filename, new_filename)
        print(f'succesfully written to {new_filename}')
    else:       
        print(f'succesfully written to {filename}')
    
welcome()               