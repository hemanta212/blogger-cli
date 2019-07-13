# Intended workflow for blogger-cli
Naturally you won't have more than 2/3 blog's to manage (Although you can manage how much blog you like).
Your blogs are accessible globally. You do not need to be in your blog's folder.

You work on one blog at a time. Make that blog default.
```
blogger setdefault <blogname>
```
Now carry out commands without specifying -b option.

It is recommentd to fill your setup configs. Carefully curate all your needed configs and you can view all configs by using the command ```blogger info```.  Also you can view your blog's config using ```blogger info <blogname>```.
Avoid passing options to commands  and instead fill your configs.

If you need to work on another blog  just switch the defaut blog to that.

## Conversion
Set up a working_dir in your config to the folder where you save your ipynb, md, html files for your blog.
Now conversion is just running
```
blogger convert
```
Please read more about it [here](customizing.md#recommended-workflow)
For safety during folder conversion read [this](customizing.md#conversion-of-folder)

## Deploying
Just to make sure things are okay and experimeting your changes run ```blogger serve``` and visit your blog from browser.

## Versioning
Keep _blogger_templates folder inside your blog for version control and global access. You can also export blog_config to your blog for versioning and to import it just run.
```
blogger config -b <blogname> -re /path/to/json/file
```
