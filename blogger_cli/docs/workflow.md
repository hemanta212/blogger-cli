# Intended workflow for blogger-cli
The intended workflow for blogger-cli is similar to git. Here is why.
It is expected that you won't have more than 2/3 blog's to manage (Although you can manage how much blog you like).
In that case your blog is accessible globally. You donot need to be in your blog's folder.

You work on one blog at a time. Make that blog default.
```
blogger setdefault <blogname>
```
Now carry out commands without specifying -b option.

It is recommentd to fill your setup configs. Carefully curate all your needed configs and you can view all configs by using the command ```blogger info```.  Also you can view your blog's config using ```blogger info <blogname>```.
You have to avoid passing options to commands  and instead fill your configs

If you need to work on another blog  just switch the defaut blog to that.
