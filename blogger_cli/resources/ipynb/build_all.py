import os
import glob
from add_static_content import convert

base_folder = "."

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

to_ignore  = ['.idea','.ipynb_checkpoints']
subdirs = get_immediate_subdirectories(base_folder)
subdirs = [x for x in subdirs if x not in to_ignore]

for s in subdirs[:]:
	year_path = os.path.join(base_folder, s)
	notebooks  = glob.glob(os.path.join(year_path, "*.ipynb"))
	for n in notebooks[:]:
		try:
			out = convert(n)
		except:
			print(n)
