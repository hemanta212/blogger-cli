class Blog:
    def __init__(self, cfg, blog):
        self.cfg = cfg
        self.blog = blog
        self.layout = {
            'apptoken': None,
            'html_dir': None,
            'ipynb_dir': None,
            'run': None,
        }
    
    def __repr__(self):
        return "configuration: {0}, blog: {1}".format(self.cfg, self.blog)
    
    def __str__(self):
        return self.blog

    def delete(self):
        try:
            blog_list = self.cfg.read(key='blogs')
        except KeyError:
            print("blog doesnot exist")
            return 0
        blog_list.remove(self.blog)
        self.cfg.delete_key(self.blog)

        if self.cfg.read(key='default') == self.blog:
            self.cfg.write('default', None)
        self.cfg.write('blogs', blog_list)

    def set_default(self, default_blog):
        config_dict = self.cfg.get_dict()
        config_dict['default']=default_blog
        self.cfg.write_dict(config_dict)

    def register(self):
        try:
            blog_list = self.cfg.read(key='blogs')
        except (KeyError, ValueError):  # Valuerror if file is empty
            blog_list = []
            self.cfg.write('blogs', [])
        blog_list.append(self.blog)
        print("registering..")
        self.cfg.write(self.blog, self.layout)
        self.cfg.write('blogs', blog_list)

    def add_key(self, key, value):
        blog_dict = self.get_dict()
        blog_dict[key] = value
        self.cfg.write(self.blog, blog_dict)

    def get_dict(self):
        return self.cfg.read(key=self.blog)

    def get_value(self, key):
        blog_dict = self.get_dict()
        return blog_dict[key]

    @staticmethod
    def blogs(cfg):
        return cfg.read(key='blogs')

    def exists(self):
        try:
            blog_list = self.cfg.read(key='blogs')
        except (KeyError, ValueError, FileNotFoundError):  # Valuerror if file is empty
            self.cfg.init_config()
            print("no blog registered yet")
            return False

        if self.blog in blog_list:
            return True
        else:
            print(self.blog, "not registered yet")
            return False

