# Conversion
Blogger uses python-markdown and nbconvert library to convert your posts to Html and injects snippets to it. Thus markdown(.md), jupyter(.ipynb) and Html(.html) are supported files.

You can convert any number of files, folder you like at once. However, they are treated as a batch i.e if you provide a topic option in command then every blog converted from that command will be under the same topic.
Various options are available to you in convert command. See all [here](#Conversion-options).


## Contents
1. [Conversion of files](#Conversion-of-files)
    - [Html files](#html-files)
    - [Code support](#code-support)
2. [Conversion of folders](#Conversion-of-folders)
3. [Static files transfer](#Static-files-transfer)
3. [Conversion options](#Conversion-option)

<a id="Conversion-of-files"></a>
## Conversion of files
Converting a file is as simple as:
```
$ blogger convert filename
```
However, blogger fills various gaps like where converted files are placed and which blogs to use from your config. See [here](blog_management.md) for how to set up configs.
for example, the above command assumes:

1. You have set a default blog and blog_dir and blog_posts_dir's value in the config,
2. File to be converted should be in the current directory.

A more flexible or independent command is (although it is recommended to setup you config)
```
$ blogger convert file1 file2 -b <blogname> -o ~/myblog.github.io/blog/
```
> The options will override the configs every time.


#### Recommended workflow
You can set a working dir in your config providing a folder you use to store your md, ipynb, Html files. Blogger will automatically convert the modified changes for you.
```
blogger config -b <blogname> working_dir /path/to/dir
```
Now you can just call ```blogger convert``` and then blogger will scan the dir and remember when the file was last scanned to detect and process modified files automatically.
You have all the options like -r, -ex-html, --topic etc available as well.

<a id="html-files"></a>
### HTML files
When a html file is passed for conversion. It is converted to html with all (navbar, analytics, disqus etc...) inserted inside it.
So there is nothing extra for you to do
```
$ blogger convert htmlfile
```

<a id="code-support"></a>
### Code support
Every file converted to Html will have mathjax and code support injected to it. You can pass --not-code option to avoid injecting them in case you don't need those.
```
$ blogger convert filename --not-code
```

For ipynb files, the converted Html won't have input/output prompts like In[1] Out[2] etc. You can enable this by editing js.html snippet. Look [here](customizing.md)

<a id="Conversion-of-folders"></a>
## Conversion of folders
If folder are specified all supported extensions(html, md, ipynb) will be picked and converted. To avoid html files just pass -ex-html/--exclude-html option. Similarly you can recursively search within any folder to get files!
```
$ blogger convert file folder/ -b <blogname>
$ blogger convert folder1/ folder2/ --exclude-html
$ blogger convert . -r --exclude-html
```
Similarly set up filter_post_without_title config to filter out 'experimental' files without title from adding into the index. However they will be converted and placed in your blog's post folder.

```
blogger config -b <blogname> filter_post_without_title true
```

<a id="Static-files-transfer"></a>
## Static files transfer
By default, blogger searches for img and video tags in Html then for:
- URI: It decodes the base64 URI to mp4 and png video and images resp.
- URL: URL in img tag are downloaded and kept in images folder but videos are left as is.
- local files: The local file references in img and video tags are resolved and copied to the blog. This applies to files of all formats both videos and audio.

You can switch all of them off by passing -no-ex or --no-extract option during conversion.
Similarly you can set the post_extract_list config.
```
blogger config -b <blogname> post_extract_list ['URI', 'URL']
blogger config -b <blogname> post_extract_list ['URL']
blogger config -b <blogname> post_extract_list ['URI']
```
1st will enable extraction of both URI and URL images, 2nd only extracts URL and leaves URI as is and third leaves URL and extracts URI images.


<a id="Conversion-option"></a>
## Conversion options
-r, --recursive :
This will search any given folder recursively to deepest file. Without this option only surface files of specified folder is converted.

--not-code:
Do not add mathjax and code support.

-o, --to:
The destination for converted files, DEFAULT from blog_config.

-b, --blog:
Name of the blog.

-ex-html, --exclude-html:
Ignore html files from conversion.

--img-dir:
Folder to store post images. Default: blog's config

-no-ex, --no-img-extract:
Disable image, video extraction from URI, URLs and local files.

--topic:
Topic in which this post should be placed in the index file. Applied to all files currently converting.

-temp, --template:
Folder path of a custom templates folder. Default 'blog_templates_dir' value in config.

--override-meta:
Ignore meta topic in favour of --topic option. More info [here](meta.md).

-v, --verbose:
Enable verbose flag for detail reporting of what's going on.

