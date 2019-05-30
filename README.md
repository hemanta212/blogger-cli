# Blogger-cli 
A custom cli tool that can process programming blogs including jupyter notebooks, markdown files, and even any custom template. Write your blog in simple text, md or jupyter notebooks and then transform into blog post with mathjax, code support, google analytics, navigation, disqus support.

## Why?
Jekyll and Pelican are mess to learn and manage and can get bulky and slow.
Blogger-cli has simple conversion system that is fast as well extremely customizable.
Blogger-cli design is for people with technical knowledge. 

## Features
* Out of the box support for github pages 
* Custom conversion of ipynb notebook with great support for mobile devices as well.
* Manage your blog entirely from command line. 
* Write and post blogs from android or any micro device. All that is required is command line with python and pip.
* Built in design, blog_templates for rapidly setting your blog from scratch
* Support for custom themes and templates

## Installation
```
$ git clone https://github.com/hemanta212/blogger-cli.git
$ cd blogger-cli
$ python -m venv venv 
```
### Activation for Windows
```
$ venv\Scripts\activate
```
### Activation for Mac or Linux
```
$ source venv\bin\activate
```
### After Activation
```
$ python -m pip install -e .
```

## Usage 
### Managing blogs
* Add -> ```$ blogger addblog <blogname>```
* Setup -> ```$ blogger setupblog <blogname>```
* Remove -> ```$ blogger rmblog <blogname>```
* Make default blog -> ```$ blogger setdefault <blogname>```

### Conversion
* Files -> ```$ blogger convert file1 file2 -b <blogname> -o ~/myblog.github.io/blog/
  > You can omit -b option by setting default blog and -o option by setting blog posts dir in its config.
