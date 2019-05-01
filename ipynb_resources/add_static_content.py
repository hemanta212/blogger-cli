import sys
import os
BASIC = True
#notebook_file = sys.argv[1]
from builtins import open
import re


home_page = "https://nipunbatra.github.io/blog/"
social = {'FB':"https://facebook.com/sharer/sharer.php?u=%s"}

def convert(notebook_file):
	# Get parent folder of file
	parent_folder = os.path.abspath(os.path.join(notebook_file, os.pardir))
	notebook_name = (os.path.splitext(notebook_file)[0]).split("/")[-1]

	from nbconvert import HTMLExporter
	import nbformat
	from traitlets.config import Config
	c = Config()
	c.HTMLExporter.preprocessors = ['nbconvert.preprocessors.ExtractOutputPreprocessor']
	#resources = {}
	# Create directory to store post files
	"""
	try:
		os.makedirs(os.path.join(parent_folder, notebook_name))
	except:
		pass
	"""

	#resources['output_files_dir'] = ''
	# create the new exporter using the custom config
	html_exporter = HTMLExporter(config=c)
	html_exporter = HTMLExporter()

	#return html_exporter


	if BASIC:
		html_exporter.template_file = 'basic'

	nb = nbformat.reads(open(notebook_file, 'r').read(), as_version=4)

	(body, resources) = html_exporter.from_notebook_node(nb)
	# FIRST between H1 in body

	from bs4 import BeautifulSoup
	soup = BeautifulSoup(body, 'html.parser')
	try:
		title = soup.find_all('h1')[0].contents[0]
		if title is None: title = "Nipun Batra"
	except:
		title="Nipun Batra"
		



	"""
	# Replace
	body = body.replace('<img src = "output_""', '<img src = "../%s/output_"' %notebook_name)

	mpl_images = resources['outputs']
	for image_name, image_binary in mpl_images.iteritems():
		with open(os.path.join(os.path.join(parent_folder, notebook_name, image_name)), 'wb') as f:
			f.write(image_binary)

	"""

	read_navbar = open("navbar.txt", 'r').read()
	read_mathjax = open("mathjax.txt", 'r').read()

	read_disqus = open("disqus.txt", 'r').read()
	read_css = open("bootstrap_css.txt", 'r').read()
	read_ga = open("google_analytics.txt","r").read()

	if BASIC:
		body = """<html>
				<head>
				<meta charset="utf-8">
			    <meta http-equiv="X-UA-Compatible" content="IE=edge">
			    <meta name="viewport" content="width=device-width, initial-scale=1">
			    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
			    <meta name="description" content="">
			    <meta name="author" content="">
			    <title>"""+title+"""</title>
			    </head>
			    <body>
			    <div class="container" margin="5%">"""+body+"</div></body></html>"




	if read_navbar not in body:
		body = body.replace("<body>", "<body>\n" + read_navbar)

	if read_ga not in body:
		body = body.replace("</body>", read_ga + "\n</body>")

	if read_disqus not in body:
		body = body.replace("</body>", read_disqus + "\n</body>")

	if read_mathjax not in body:
		body = body.replace("</head>", read_mathjax + "\n</head>")

	if read_css not in body:
		body = body.replace("</title>", "</title>\n" + read_css)
		body = body.replace("</body>", read_css + "\n</body>")


	# Put social media icons
	#body = body.replace("img src", "img width='100%' src")


	#body = body.replace(" rendered_html", "")
	body = body.replace(".rendered_html{overflow-x:auto" , ".rendered_html{overflow-x:auto;overflow-y: hidden;")
	body = body.replace("#notebook{font-size:14px;line-height:20px;", "#notebook{font-size:20px;line-height:29px;")
	body = body.replace("div.text_cell_render{outline:0;resize:none;width:inherit;border-style:none;padding:.5em .5em .5em .4em;color:#000;",
	                    "div.text_cell_render{outline:0;resize:none;width:inherit;border-style:none;padding:.5em .5em .5em .4em;color:#777;")





	html_file = notebook_file.replace(".ipynb", ".html")
	html_file_writer = open(html_file, 'w')
	html_file_writer.write(body)
	html_file_writer.close()
