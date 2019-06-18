class BloggerMessage(object):

    main = '''\
Usage: cli [OPTIONS] COMMAND [ARGS]...

  A CLI tool to maintain your blogger blog. Sync, convert and upload :).

Options:
  -v, --verbose  enables verbose command
  --help         Show this message and exit.

Commands:
  addblog     Register a new blog
  config      Change a blog's configurations
  convert     Convert files to html
  export      Export default design to your blog
  info        Show blog's properties
  rmblog      Remove a blog
  setdefault  Set a blog as default
  setupblog   Register a new blog
'''

    addblog_success = '''\
Blog added succesfully
'''

    addblog_existing = '''\
Blog already exists!
'''

    rmblog_success = '''\
Blog removed succesfully
'''

    info_success = '''\

Registered Blogs:
   test1

Blog:configs [standard]
   blog_dir
   blog_images_dir
   blog_posts_dir
   default
   disqus_username
   google_analytics_id
   templates_dir
   working_dir

Tip: Use blogger info blogname for blog details
'''
