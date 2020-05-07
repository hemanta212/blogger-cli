# Serving Blog Locally
The serve command serves your blog locally. You blog is visible for every device in the same LAN or connected with the same wifi.

It takes blogname as argument which is optional if you have a default blog set.
```
blogger serve <blogname>
blogger serve <blogname> --dir literally/any/folder/ -p 8989 
```

## Options

- -d, --dir:
Folder path to serve. By default, it is the blog_dir value in blog's config

- -p, --port:
Port to host on. Default is 8000. It appears in URL as http://localhost:port 
Blogger will error out if port isn't available. In that case you can just omit
the --port option and blogger will pick free ports in range 8000-8999 (inclusive)

- --verbose, -v:
Enable verbosity for more information on the process.
