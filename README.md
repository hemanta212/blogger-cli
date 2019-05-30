# Blogger-cli 
A custom cli tool that can process programming blogs including jupyter notebooks, markdown files, and even any custom template. Write your blog in simple text, md or jupyter notebooks and then transform into blog post with mathjax, code support, google analytics, navigation, disqus support.


## Why?
It is easy to get your hands on, works flawlessly and won't get bulky and slow overtime.
Blogger-cli has simple conversion system that is fast as well extremely customizable. 


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


## Getting Started
Make a website repository and clone it to your computer. Now register your blogname with blogger
```$ blogger addblog <blogname>```
and setup necessary configs. Now, If you have new site or empty site. You can get blogger default design and boiler plate.
```
$ blogger export blog_template -b <blogname> 
``` 
Now, all assets will be moved to the blog_dir you specified in the blog config during setup.

If you just need blog posts index page (list of blog links). You can get it.
```
$ blogger export blog_index -b <blogname>
```

Similarly if you only need the design assets (css, js, fonts) of jupyter notebook or md files.
```
$ blogger export design_assets -b <blogname> -o assets/  
```
  > TIP: More detail on these export commands down below.


## Usage 
### Managing blogs
* ```$ blogger addblog <blogname>```
* ```$ blogger setupblog <blogname>```
* ```$ blogger rmblog <blogname>```
* ```$ blogger setdefault <blogname>```

### Conversion
#### Files
* ```$ blogger convert file1 file2 -b <blogname> -o ~/myblog.github.io/blog/```
    > -b option can be omitted by setting a default blog. Other options can be omitted by setting up configs for respective blogs.  
* ``` $ blogger convert filename ```
 
#### Html files
When a html file is passed for conversion. It is converted to html with all (navbar, analytics, disqus etc...) inserted inside it.
* ``` $ blogger convert file.html```

#### Folders
If folder are specified all supported extensions(html, md, ipynb) will be picked and converted. To avoid html files just pass --no-html option.
* ``` $ blogger convert file folder/ -b <blogname>```
* ``` $ blogger convert folder1/ folder2/ --no-html```

#### Code support
Every file converted to html will have mathjax and code support injected to it. You can pass --not-code option to avoid injecting them incase you don't need those.
```
$ blogger convert filename --not-code 
```

### Configurations

#### Settting

You can get all registered blogs and configs that you can view and set by running 
* ```$ blogger info```

Set configs by:
* ``` $ blogger config -b <blogname> blog_dir  ~/username.github.io/```
    > -b option can be omitted by setting default blog

After setting blog_dir config other config such as blog_posts_dir should be relative to blog_dir as root.
* ``` $ blogger config blog_posts_dir /posts``` 
      
#### View
```
$ blogger info <blogname> 
```

### Export command
The export command helps to export resources including configs, indexes, template, design etc.
To view various resources that you can export, run:
* ``` $ blogger export --help ```

General exports,
```
$ blogger export -b <blogname> blog_template -o ~/username.github.io/
```
You can shorten it to:
```
$ blogger export blog_template 
```

When using -o option here in export, it refers to relative path from root blog dir unless you start from root.
```
$ blogger export design_assets -o /assets/
$ blogger export desing_assets -o ~/test/folder1/
```
