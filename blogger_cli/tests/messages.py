class BloggerMessage(object):

    main = """\
Usage: cli [OPTIONS] COMMAND [ARGS]...

  A CLI tool to maintain your jupyter notebook blog.

Options:
  -v, --verbose  enables verbose command
  --help         Show this message and exit.

Commands:
  addblog     Register a new blog
  addfeed     Write to rss/atom feed
  config      Change a blog's configurations
  convert     Convert files to html
  export      Export default design to your blog
  info        Show blog's properties
  rmblog      Remove a blog
  serve       Serve your blog locally
  setdefault  Set a blog as default
  setupblog   Register a new blog
  spellcheck  Check spelling errors
  uninstall   Uninstall the custom installation
  update      Update the custom installation
"""

    addblog_success = """\
Blog added succesfully
"""

    addblog_existing = """\
Blog already exists!
"""

    rmblog_success = """\
Blog removed succesfully
"""

    info_success = """\

Blogger-cli version: 1.2.1

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

"""
    all_info_success = """\

Blogger-cli version: 1.2.1

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
   feed_file
   site_url
   md_summary_limit
   ipynb_summary_limit

Tip: Use blogger info blogname for blog details

"""

    spellcheck_help = """\
Usage: cli spellcheck [OPTIONS] FILENAME

  This command will check spelling and point out the typos.

Options:
  -f, --force_suggestions
  --help                   Show this message and exit.
"""

    addfeed_help = """\
Usage: cli addfeed [OPTIONS] [FILE_PATH]

Options:
  -rss                Generate rss file
  -i, --interactive   Edit feed entry editor
  -t, --title TEXT    Title of post
  -c, --content TEXT  Content for mail or [File path] for content
  -v, --verbose
  --setup             Setup feed for first time
  -b, --blog TEXT     Name of blog
  --help              Show this message and exit.
"""
