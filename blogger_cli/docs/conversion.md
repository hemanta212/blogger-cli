# Conversion
Blogger uses python-markdown and nbconvert library to convert your posts to html and injects snippets to it. Thus markdown, jupyter and html are supported files.

You can convert any number of files, folder you like at once. However they are treated as a batch i.e if you provide a topic option in command then every blog converted from that command will be under same topic.
Various options are available to you in convert command. See all [here](#Conversion-options).

As of now, you cannot place original and converted files in same folder. So do not run convert command from your blog's folder.

## Contents
1. Conversion of files
    - html files
    - code support
2. Conversion of folders
3. Conversion options

## Conversion of files
Converting a file is simple as: 
```
$ blogger convert filename
```
However blogger fills various gaps like where converted files are placed and which blogs to use from your config.
for example the above command assumes you have set a [default blog](#todo) and [blog_dir and blog_posts_dir](#todo) in config,
also the file to be converted should be in current directory.

A more flexible or independent command is (although it is recommended to setup you config)
```
$ blogger convert file1 file2 -b <blogname> -o ~/myblog.github.io/blog/
```
    > The options will override the configs everytime.

### Html files
When a html file is passed for conversion. It is converted to html with all (navbar, analytics, disqus etc...) inserted inside it.
So there is nothing extra for you to do
```
$ blogger convert htmlfile
```
### Code support
Every file converted to html will have mathjax and code support injected to it. You can pass --not-code option to avoid injecting them incase you don't need those.
```
$ blogger convert filename --not-code 
```

## Conversion of folders
If folder are specified all supported extensions(html, md, ipynb) will be picked and converted. To avoid html files just pass --no-html option. Similarly you can recursively search within any folder to get files!
``` 
$ blogger convert file folder/ -b <blogname>
$ blogger convert folder1/ folder2/ --exclude-html
$ blogger convert . -r --exclude-html
```

## Conversion options
-r, --recursive :
This will search any given folder recursively to deepest file. Without this option only surface files of specified folder is converted.

--not-code:
Do not add mathjax and code support.
  
-o, --to:
Destination for converted files, DEFAULT from blog_config.
  
-b, --blog:
Name of the blog.

-ex-html, --exclude-html:
Ignore html files from conversion.
  
--img-dir:
Folder for post images. Default: blog's config
  
-no-imgex, --no-img-extract:
Disable image extraction from URI and urls.

--topic:
Topic in which this post should be placed in index. Applied to all files currently converting.

-temp, --template:
Folder path of custom template. Default 'blog_templates_dir' value in config.

--override-meta:
Ignore meta topic in favour of --topic option. More info [here](#todo).
  
-v, --verbose:
Enable verbose flag for detail reporting of what's going on.

