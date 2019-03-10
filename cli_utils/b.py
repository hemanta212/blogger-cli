import sys
import os

from converter import convert
#ipynb_path = input("default jupyter_files dir [%USERPROFILE%/DESKTOP]")
file_path = "F:/my_projects/jupyter_notebooks/data_science/"
os.chdir(file_path)
for f in os.listdir():
	try:
		file_list = f.split(".")
		if "ipynb" in file_list:
			convert(f)
	except:
		continue;

