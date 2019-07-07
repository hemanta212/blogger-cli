# Exporting resources to your blog
This command export resources that you can use to quickly setup your blog.
When you export resources existing folder of same name will be replaced permanently, there is no going back. So always do this in empty folder or use -o option to place them in test/ folder.

Following files/folder can be replaced: 
1. index.html
2. css/
3. js/
4. fonts/
5. images/
6. \_blogger\_templates/

Use ```blogger export --help``` to view items that can be exported.

# Contents
1. [Exporting blog template](#Exporting-blog-template)
2. [Exporting blog index](#Exporting-blog-index)
3. [Exporting blog assets](#Exporting-blog-assets)
4. [Exporting blog configurations](#Exporting-blog-configurations)

# Exporting blog template
Blog template consists of assets(css and js), blog index, website index, images dir, _blogger_templates, blog directory to quickly set you up with a up and running site. You can customize this css as you like and indexes considering some procedure described [here](todo).
```
blogger export -b <blogname> blog_template
```
You can also specify a custom folder using -o option. It is relative from blog root folder however you can alsospecify other folder using absolute path from begining.
```
blogger export -b <blogname> blog_template -o test/
blogger export -b <blogname> blog_template -o ~/my_website_folder/test/
```

# Exporting blog index
If you just want blog index,
```
blogger export -b <blogname> blog_index
```
The -o option rule is same as exporting blog_template mentioned above.
```
blogger export -b <blogname> blog_index -o blog/ 
blogger export -b <blogname> blog_index -o ~/my_website/test
```

# Exporting blog assets
If you just want blog assets (css, js, fonts). For default support export them inside assets/ folder
```
blogger export -b <blogname> blog_assets -o assets/
```
> If you export css, js in different folder you have to override the default templates with new path. More info [here](#todo)

The -o option rule is same as exporting blog_template mentioned above.
```
blogger export -b <blogname> blog_assets -o assets/ 
blogger export -b <blogname> blog_assets -o ~/my_website/assets/
```

# Exporting blog configurations
If you just want blog config,
```
blogger export -b <blogname> blog_config
```
The -o option rule is same as exporting blog_template mentioned above.
```
blogger export -b <blogname> blog_config -o config/ 
blogger export -b <blogname> blog_config -o ~/my_website/test
```
If you want config of all blogs. copy ~/.blogger/blog_config.cfg to your folder.
