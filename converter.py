import sys
import os
BASIC = True
from builtins import open
import re
#from gmailsender import send_email

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
		if title is None:
		     title = "Pykancha"
	except:
		title="PYKANCHA"

	
	if BASIC:
		body = '''<style>
body {
    font-family: "News Cycle", "Arial Narrow Bold", sans-serif;
    font-size: 21px;
    line-height: 1.42857143;
    color: #777777;
    background-color: #ffffff;

}
a.anchor-link:link {
    text-decoration: none;
    padding: 0 20px;
    visibility: hidden
}

h1:hover .anchor-link,
h2:hover .anchor-link,
h3:hover .anchor-link,
h4:hover .anchor-link,
h5:hover .anchor-link,
h6:hover .anchor-link {
    visibility: visible
}
th,
td {
    padding: 8px;
}

tr:hover {
    background-color: #f5f5f5
}
div.cell {
    padding: 4px
}
pre {
    font-size: 15px;
    display: block;
    padding: 8.5px;
    margin: 0 0 9px;
    font-size: 12px;
    line-height: 1.42857143;
    word-break: break-all;
    word-wrap: break-word;
    color: #333333;
    background-color: #f5f5f5;
    border: 1px solid #ccc;
    border-radius: 2px;
    
}
pre code {
  padding: 0;
  font-size: inherit;
  color: inherit;
  white-space: pre-wrap;
  background-color: transparent;
  border-radius: 0;
}
.pre-scrollable {
  max-height: 340px;
  overflow-y: scroll;
}
div.input_prompt {
    color: firebrick;
}

div.output_prompt {
    color: firebrick;
}
img {
    max-width: 100%
}
</style>
    <!-- MathJax configuration -->
    <script type="text/x-mathjax-config">
    MathJax.Hub.Config({
        tex2jax: {
            inlineMath: [ ["$","$"], ["\\(","\\)"] ],
            displayMath: [ ["$$",'$$'], ["\\[","\\]"] ],
            processEscapes: true,
            processEnvironments: true
        },
        // Center justify equations in code and markdown cells. Elsewhere
        // we use CSS to left justify single line equations in code cells.
        displayAlign: 'center',
        "HTML-CSS": {
            styles: {'.MathJax_Display': {"margin": 0}},
            linebreaks: { automatic: true }
        }
    });
    </script> ''' + body + '''<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

  ga('create', 'PUT YOUR CODE HERE', 'auto');
  ga('send', 'pageview');

</script><script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

  ga('create', 'PUT YOUR CODE HERE', 'auto');
  ga('send', 'pageview');

</script>'''



#	if read_basic not in body:
#		body = body.replace("</script>", "</script>\n" + read_basic)



	# Put social media icons
	#body = body.replace("img src", "img width='100%' src")


	body = body.replace(" rendered_html", "")
	body = body.replace(".rendered_html{overflow-x:auto" , ".rendered_html{overflow-x:auto;overflow-y: hidden;")
	body = body.replace("#notebook{font-size:14px;line-height:20px;", "#notebook{font-size:20px;line-height:29px;")
	body = body.replace("div.text_cell_render{outline:0;resize:none;width:inherit;border-style:none;padding:.5em .5em .5em .4em;color:#000;",
	                    "div.text_cell_render{outline:0;resize:none;width:inherit;border-style:none;padding:.5em .5em .5em .4em;color:#777;")





	html_file = notebook_file.replace(".ipynb", ".html")
	html_file_writer = open(html_file, 'w')
	html_file_writer.write(body)
	html_file_writer.close()
	##send_email(body)