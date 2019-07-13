# Blogger-cli
A custom cli tool to process jupyter notebooks, markdown files and html files. Write your blog in markdown or jupyter notebooks and then transform into blog post with mathjax, code support, google analytics, navigation, disqus support.


## Why?
It is easy to get your hands on, works flawlessly and won't get bulky and slow overtime.
Blogger-cli has simple conversion system that is fast as well extremely customizable. 


## Features
* Robust conversion of ipynb notebooks with great support for mobile devices as well.
* Built in support for disqus, google analytics, navigation bar, mathjax and code highlighting.
* Blog management: updating index, parsing out images, managing topics and metadata. 
* Write and post blogs from android or any micro device. All that is required is command line with python and pip.
* Built in design, blog_templates for rapidly setting up your blog from scratch.
* Fully customizable with support for custom themes and templates
* Also support conversion of other file formats like markdown. You can also implement your own.


## 💻 Installation

### Recommended Method
```
$ curl -sSL https://raw.githubusercontent.com/hemanta212/blogger-cli/master/get_blogger.py | python
```
Since blogger has alot of dependecies (nbconvert, jupyter), this custom installer will install in a virtualenv and add it to your path for global access!.

### Using pip
```
pip install blogger-cli
```

If you mainly use jupyter notebook, then you already have all dependecies although it is recommende to use virutalenv.


## 🚀 Getting Started
Make a website repository and clone it to your computer. Now register your blogname with blogger
```$ blogger addblog <blogname>```
and setup necessary configs. Now, If you have new site or empty site. You can get blogger default design and boiler plate.
```
$ blogger export blog_layout -b <blogname>
```
Now, all assets will be moved to the blog_dir you specified in the blog config during setup.
```
$ blogger serve <blogname>
```
Open the url http://localhost:8000/ in your browser to view your blog!!

## 📖 Documentation
- [Installation, update, uninstall methods](blogger_cli/docs/installation.md)
- [Managing blogs and configurations](blogger_cli/docs/blog_management.md)
- [Conversion of files and folders](blogger_cli/docs/conversion.md)
- [Serving blog locally](blogger_cli/docs/serving_blog_locally.md)
- [Using export command](blogger_cli/docs/export.md)
- [Customizing templates and design](blogger_cli/docs/customizing.md)
- [Writing blog's metadata](blogger_cli/docs/meta.md)
- [Recommended workflow for blogger-cli](blogger_cli/docs/workflow.md)

## Author

👤 **Hemanta Sharma**
- Github: [@hemanta212](https://github.com/hemanta212)

## Special Thanks

👤 **Nipun Batra** : Inspiration for core conversion mechanism and design resources.
- Github: [@nipunbatra](https://github.com/nipunbatra)
- His article on ipynb conversion: [@nipunbatra.github.io](https://nipunbatra.github.io/blog/2017/Jupyter-powered-blog.html)

## Show your support

Please ⭐️ this repository if this project helped you!

## 📝 License
Copyright © 2019 [Hemanta Sharma](https://github.com/kefranabg).<br />
This project is [MIT](LICENSE) licensed.
---
