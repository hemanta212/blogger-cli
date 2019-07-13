# Serving Blog Locally
The serve command serves your blog locally. You blog is visible for every device in same LAN or connected with same wifi.

It takes blogname as argument which is optional if you have a default blog set.
```
blogger serve <blogname>
blogger serve <blogname> --dir literally/any/folder/ -p 8989 
```

## Options

- -d, --dir:
Folder path to serve. By default, it is the blog_dir value in blog's config

- -p:
Port to host on. Default is 8000. It appears in url like, http://localhost:port

--verbose, -v:
Enable verbosity for more information on the process.
