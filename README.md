# Blogger-cli
A custom cli tool to process jupyter notebooks, markdown files and html files. Write your blog in markdown or jupyter notebooks and then transform into blog post with mathjax, code support, google analytics, navigation, disqus support.

See a sample blog made by blogger-cli: [Here](https://pykancha.github.io/test/)

## Why?
It is easy to get your hands on, works flawlessly and won't get bulky and slow overtime.
Blogger-cli has a simple conversion system that is fast as well as extremely customizable. 


## Features
* Robust conversion of ipynb notebooks with great support for mobile devices as well.
* Built-in support for disqus, google analytics, navigation bar, social sharing, mathjax and code highlighting.
* Blog management: updating index, parsing out images, managing topics and metadata. 
* Write and post blogs from android or any micro device. All that is required is command line with python and pip.
* Built in design, blog_templates for rapidly setting up your blog from scratch.
* Fully customizable with support for custom themes and templates
* Also support conversion of other file formats like markdown. You can also implement your own.


## 💻 Installation

### Recommended Method
```
$ curl -sSL https://hemanta212.github.io/blogger-cli/get_blogger.py | python
```
Since blogger has alot of dependecies (nbconvert, jupyter), this custom installer will install them in a virtual environment and add it to your path for global access.

### Using pip
```
pip install blogger-cli
```

If you mainly use jupyter notebooks, then you already have all the required dependencies although it is recommended to use `virutal environments`.


## 🚀 Getting Started
Make a website repository and clone it to your computer. Now register your blog name with blogger
```$ blogger addblog <blogname>```
and setup necessary configs. Now, If you have new site or empty site. You can get blogger default design and boilerplate.
```
$ blogger export blog_layout -b <blogname>
```
Now, all assets will be moved to the blog_dir you specified in the blog config during setup.
```
$ blogger serve <blogname>
```
Open the url http://localhost:8000/ in your browser to view your blog!!

## 📖 Documentation
- [Installation, update, uninstall methods](docs/installation.md)
- [Managing blogs and configurations](docs/blog_management.md)
- [Conversion of files and folders](docs/conversion.md)
- [Serving blog locally](docs/serving_blog_locally.md)
- [Using export command](docs/export.md)
- [Customizing templates and design](docs/customizing.md)
- [Writing blog's metadata](docs/meta.md)
- [Recommended workflow for blogger-cli](docs/workflow.md)

> View docs in: [website](https://hemanta212.github.io/blogger-cli/)

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
