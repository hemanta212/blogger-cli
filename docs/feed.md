<a id="orgad6581f"></a>
# Feeds in blogger

# Table of Contents

1.  [Introduction](#org44119c8)
2.  [Creating a feed.](#org9ef5f13)
3.  [Using an existing feed.](#org04b5e16)
    1.  [Adding entries](#orgc51c26e)
    2.  [Duplicate entries/ Updating entries:](#orga2fcc10)


<a id="org44119c8"></a>


## Introduction

The feed is a feature you can use to generate rss/atom feed for your blog.
With this you'll be able to:

-   Generate a new rss/atom feed from scratch.
-   Use an existing rss/atom feed to append entries to it.
-   Specify a default feed file to be used by blogger, thus manage multiple feed files.

To use, let's start by setting config file in config.

    $ blogger config -b <blogname> feed_file path/to/feed/file

Of course, the file doesnot have to exist. If you want the feed file to be out of your blog folder,
you need to provide absolute path. Other path will simply be interpreted relative to blog_dir.

    #1. This resolves to blog_dir/blog/feed.xml
    $ blogger config -b <blogname> feed_file blog/feed.xml 
    
    #2. This resolves to ~/.my_files/feed.xml
    $ blogger config -b <blogname> feed_file ~/.my_files/feed.xml

Similary, you can also set 'site_url' config now with your website name which helps to resolve absolute link of your post.


<a id="org9ef5f13"></a>

## Creating a feed.

If you don't have a feed for your blog, you can create one using:

    #1. creates atom feed by default
    $ blogger addfeed -b <blogname> --setup
    
    #2. To create rss feed
    $ blogger addfeed -b <blogname> --setup -rss

You'll be prompted to set feed file path if you haven't already. A set of questions will be asked to setup your feed.


<a id="org04b5e16"></a>

## Using an existing feed.

Whether you created feed file with blogger or had existing feed file, you should be able to add entries to it.
The type of feed file will be automatically determined. Entries will be appended to it as you add your posts to it.
However, note that the indentation of whole file will change to two space indentation.

<a id="orgc51c26e"></a>

### Adding entries

A normal entry consists of:

-   title
-   content [optional]  # summary or even the whole post.
-   link

You have to provide a file argument to addfeed command which SHOULD be inside your blog and MUST have ".html" extension. The 'link' is then automatically interpreted.
However you have to provide --title/-t and --content/-c option. You can omit --content option if you want.
Blogger has -i/--interactive command as well if you want to set title and content in your default editor.

    $ blogger addfeed -b <blogname> file/path --title MYPOST --content HI
    $ blogger addfeed -b <blogname> file/path --title "Only Title"

Now, if the file was converted by blogger(version >=1.2) then blogger can automatically fill title and content too as metadata 'title', 'content'(if any) are cached after conversion. This file is in '~/.config/blogger_cli/<blogname>/meta.json' file. To control what goes to content see [content options](#content_options)

Of course you can always override those cached title and content by passing the --title and \--content option to addfeed command.

    $ blogger addfeed -b <blogname> file/path


<a id="orga2fcc10"></a>

### Duplicate entries/ Updating entries:

In a feed, 'blogger' identifies entries by their links. When it encounters duplicate entry in 'addfeed' command then it simply deletes the old and updates it with current one.
'blogger' however, keeps the id's('id' in atom and 'guid' in rss feeds) of feed entries unchanged.


<a id="content_options"></a>

### Content options
You can control what summary is extracted and cached for markdown and ipynb file. As of now, summary extraction is not available for html file however manual entries are supported.

You can control the maximum number of charectars to inclue from md and ipynb post. Similary for ipynb you can specify nth markdown cell (where n is a integer).

To specify you need to set 'md_summary_limit' and 'ipynb_summary_limit' config keys. The value is number. 1000 charectars is default for md files.

    $ blogger config -b <blogname> md_summary_limit 100
    $ blogger config -b <blogname> ipynb_summary_limit 200

In ipynb files the charectar limit applies from 2nd md cell. The first md cell is assumed to be title and left out from summary.

Similarly to set cell no in ipynb you can use c[1,2,3] eg: c1, c2 to select 1st and 2nd markdown cell's text respectively. The default value is c2 for every ipynb file.

    # Selects second markdown cell in notebook
    $ blogger config -b <blogname> ipynb_summary_limit c2

