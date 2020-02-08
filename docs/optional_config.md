# Optional configs
These optional configs help you to control blogger-cli's certain behaviour. They are not meant to be
changed frequently, try to keep them consistent. All of them are handled through the config command.

    $ blogger config -b <blogname> config_name value

All config names can be listed through 'info' command passing option '--all'

    $ blogger info --all

## Meta format
The 'meta_format' config determines the comment format for meta in md and ipynb files).
The default is '<!-- -->' format. You can specify new meta_format by using the config command.
A meta format has a beginning pattern then space and ending pattern. The beginning and ending pattern can be the same but not necessarily.

    $ blogger config -b <blogname> meta_format '*/ /*'

## Post extract list
The 'post_extract_list' controls what static resource is extracted.
The static resources are images and videos. Blogger by default downloads images from URL and converts URI images to png. You can set post_extract_list config to control what gets extracted.

```
$ blogger config -b <blogname> post_extract_list ['URI', 'URL']
$ blogger config -b <blogname> post_extract_list ['URL']
$ blogger config -b <blogname> post_extract_list ['URI']
```

1st will enable extraction of both URI and URL images, 2nd only extracts URL and leaves URI as is and third leaves URL and extracts URI images.

## Filter post without title
'filter_post_without_title' config is either true or false. It will filter or prevent all those posts that don't have
a title from indexing in the index. However, this doesn't prevent or stop the conversion of the file in any way. It will not be present in index.html.

## Working dir timestamp
It is the datetime in timestamp form. It represents the last datetime when working dir was checked by blogger. It's mainly for internal use.

## Index div name
'index_div_name' is the name of the class of the posts list in index.html file of a blog. This helps to add entries there. This assumes that the list of posts is inside a div. The div's class is given so blogger can get that container and append entries to it.

## Create nbdata file
'create_nbdata_file' is config accepting 'true' or 'false'. Enabling it will create nbdata file from meta found in original ipynb file. It will have every key value from metadata. Similarly, the nbdata file will have the same name as ipynb file but '.nbdata' file extension. By default, it is 'true'.

## Delete ipynb meta
By default, blogger deletes the meta present in ipynb file after reading it and writes to a separate nbdata file. This can be controlled by setting 'delete_iynb_meta' config. The default value is 'true'.

## Feed file
This is the location of the feed file for your blog. The 'addfeed' command will use it. The value of 'feed_file' if given relative will be interpreted with respect to blog_dir otherwise if the absolute path is given, that will be used.

## Site URL
'site_url' is the URL of your website. It is used for feed to resolve and construct feed_entries URL and feed's URL itself.

## Md summary limit
This is limit in no of characters to include in the extraction of summary for md. While converting md files blogger extracts the summary, title and keeps a cache for later use in 'addfeed' command.
You can control how much character to include in summary by setting this config. The default value is 1000

    $ blogger config -b <blogname> md_summary_limit 1000

## Ipynb summary limit
This limit is similar to md. Here the text is extracted from each markdown cells except 1st one and joined. The first one is reserved for the title so it isn't included in the summary. Then the character limit is used in that to construct a summary. The value is in integer.

    $ blogger config -b <blogname> ipynb_summary_limit 1000

However, you can also specify which cell number to be used using 'c' before the cell number.
The default is c2. ie 2nd  markdown cell is used in summary

    $ blogger config -b <blogname> ipynb_summary_limit c2
