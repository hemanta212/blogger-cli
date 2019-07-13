# Managing the blog
Blogger-cli is primarily a conversion tool. So the blog management is more like config holder for your website's folder.

# Contents
1. [Registering a blog](#Registering-a-blog)
2. [Editing blog configs ](#Editing-blog-configs)
    - [Editing in bulk](#Editing-in-bulk)
    - [Editing individually](#Editing-individually)
3. [setting default blog](#Setting-default-blog)
4. [removing a blog](#Removing-a-blog)

# Registering a blog
'blogs' need to be registered first. You can do so by:
```
blogger adddblog <blogname>
```
You will be asked series of questions you can answer them or skip over them using 'n'
Similary if you want to avoid getting asked these questions and only want to register a blog use
```
blogger addblog <blogname> -s
```
You can always setup configs later

# Editing blog config
A registered blog has number of configs you can edit.

'blog_dir':
This is the main folder of your website. This folder is not used to store converted html blogs since it is treated as root website folder.
eg values: '~/my_website_folder/', 'C:\Useres\Desktop\'

'blog_posts_dir':
This is the folder you want to keep your converted blog posts in. It is specified in respect to blog_dir folder (root dir).

Example values: 'blog/', 'posts/'.

> Do not use '/' infront of folder name like '/blog/'. It conveys different meaning.


'blog_images_dir':
Where you want to store your images that we extract for you from http/s urls and data URI in your post. The path value is relative from root dir (blog_dir) same like blog_posts_dir. Images will be stored in folders with same name as your blog title and If you have topic then it will be used too. like topic/blog_title/.

Example values: 'images/blog/', 'images/', 'blog/images/'.

> For sites like github pages, you need to keep 'images' folder in root folder of your website.


'disqus_username':
If you have a disqus account you can enter username here and commenting system will work on every posts. You can get it from disqus account url. eg https://badboy11.disqus.com 's username will be 'badboy11'.

'google_analytics_id':
It is a snippet provided by google to analyze your website's traffic. Sign in and get a snippet and you can get id from there. eg: 'UA-159824128-0'

'templates_dir':
It is the directory where you can override default html templates to suit your needs. More info [here](customizing.md).

## Editing in bulk
To edit all configs in bulk, you can run:
```
blogger setupblog <blogname>
```
To skip without making any changes, type 'n' and press enter. To delete a VALUE from config, type one or many space and press enter.

## Editing individually
Use blogger info  to view all config options for a blog then,
```
blogger config -b <blogname> [config option]  [value]
```
To view a value of a config,
```
blogger config -b <blogname> [config option]
```
If nothing shows up. Your value is empty.
Similarly to delete a config,
```
blogger config -b <blogname> -rm [config option]
```
You can remove a default property of blog as well.
```
blogger config -b <blogname> -rm default
```
> Never use this to make some blog as a default blog instead use [setdefault](#Setting-default-blog) command.

# Setting default blog:
To set a blog as the default, use:
```
blogger setdefault <blogname>
```
Once a blog is set as default you do not need to specify a blog or -b parameter to ANY commands!. If you want to set another blog as the default, use:
```
blogger setdefault <anotherblogname>
``` 
Everything will safely handled. If for some reason you don't want to set any blog as default use [config command](#Editing-individually) to delete the default property.

# Removing a blog
You will lose everything if you do so.
```
blogger rmblog <blogname>
```
It only accepts one blog at a time.
