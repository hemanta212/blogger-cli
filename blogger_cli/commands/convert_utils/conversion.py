import os


def gen_conversion_class(ctx):

    class Conversion(ctx):
        def __init__(self, file_map_ext, exclude_html, iscode,
                    extract_img, img_dir):
            self.exclude_html = exclude_html
            self.extract_img = extract_img
            self.img_dir = img_dir
            self.file_map_ext = file_map_ext
            self.iscode = iscode


        def set_files_being_converted(self, path):
            isfolder = lambda x: True if os.path.isdir(x) else False
            all_files = []
            for item in path:
                if isfolder(item):
                    item = self.get_all_files(item)
                    all_files + item
                else:
                    all_files.append(item)

            self.files_being_converted = all_files


        @staticmethod
        def get_all_files(folder):
            files = []
            for file in os.listdir(folder):
                if os.path.isfile(file):
                    files.append(file)
            return files


        def check_and_ensure_dest_dir(self, output_dir):
            blog  = self.current_blog
            destination_dir = self.config.read(key=blog + ' : blog_posts_dir')

            if output_dir:
                destination_dir = output_dir

            if destination_dir is None:
                self.log("No destination folder given. Specify one with -o option or",
                    "setup in your", blog, "blog's config")
                self.exit("ERROR: NO OUTPUT FOLDER")

            destination_dir = os.path.normpath(os.path.expanduser(destination_dir))
            self.destination_dir = destination_dir


        def set_current_blog(self, blog):
            current_blog = self.default_blog
            if blog:
                current_blog = blog

            if not self.blog_exists(current_blog):
                self.log("Blog name not given. Use --blog option or set default blog")
                self.exit("ERROR: Blogname unavailable. SEE blogger convert --help")

            self.current_blog = current_blog


        def set_file_ext_map(self):
            files = self.files_being_converted
            file_ext_map = {}

            if self.exclude_html:
                self.SUPPORTED_EXTENSIONS.remove('html')

            for file in files:
                ext = get_file_ext(file)
                if ext in self.SUPPORTED_EXTENSIONS:
                    file_ext_map[file] = ext
                else:
                    self.log("Unsupported ext", ext, "Skipping")
                    continue

            self.file_ext_map = file_ext_map


        def get_file_ext(file):
            extension = os.path.splitext(file)[1]
            return extension[1:]


    return Conversion
