import sys
import os

from ipynb_to_html import convert
#ipynb_path = input("default jupyter_files dir [%USERPROFILE%/DESKTOP]")
file_path = "F:/my_projects/jupyter_notebooks/blog/"
os.chdir(file_path)
for f in os.listdir():
    try:
        file_list = f.split(".")
        if "ipynb" in file_list:
            convert(f)
    except:
        continue;

