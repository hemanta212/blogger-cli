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
  uninstall   Uninstall the custom installation
  update      Update the custom installation

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

Blogger-cli version: 1.1.0

Registered Blogs:
   test1

Blog:configs [standard]
   google_analytics_id
   disqus_username
   blog_images_dir
   templates_dir
   blog_posts_dir
   default
   working_dir
   blog_dir

Tip: Use blogger info blogname for blog details

'''
    all_info_success = '''\

Blogger-cli version: 1.1.0

Registered Blogs:
   test1

Blog:configs [standard]
   google_analytics_id
   disqus_username
   blog_images_dir
   templates_dir
   blog_posts_dir
   default
   working_dir
   blog_dir

Optional:configs [Advanced]
   meta_format
   post_extract_list
   index_div_name
   filter_post_without_title
   working_dir_timestamp
   create_nbdata_file
   delete_ipynb_meta

Tip: Use blogger info blogname for blog details

'''
