class BloggerMessage(object):

    main = '''\
Usage: blogger [OPTIONS] COMMAND [ARGS]...

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
  serve       Serve your blog locally
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
  No blog registered yet!

Blog:configs [standard] 	Optional:configs [Advanced]
   google_analytics_id 		 meta_format
   disqus_username 		 post_extract_list
   blog_images_dir 		 index_div_name
   templates_dir 		 filter_post_without_title
   blog_posts_dir 		 working_dir_timestamp
   default
   working_dir
   blog_dir

Tip: Use blogger info blogname for blog details

'''
