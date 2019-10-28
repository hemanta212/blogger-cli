# Exporting resources to your blog
This command exports resources that you can use to quickly set up your blog.
When you export resources existing folder of the same name will be replaced permanently, there is no going back. So always do this in an empty folder or use -o option to place them in test/ folder.

Note that while exporting files like blog_config and blog_index you cannot rename the file with -o option. You can rename after conversion.

Following files/folder can be replaced:
1. index.html
2. css/
3. js/
4. fonts/
5. images/
6. \_blogger\_templates/

Use ```blogger export --help``` to view items that can be exported.

# Contents
1. [Exporting blog layout](#Exporting-blog-layout)
2. [Exporting blog index](#Exporting-blog-index)
3. [Exporting blog assets](#Exporting-blog-assets)
4. [Exporting blog configurations](#Exporting-blog-configurations)
1. [Exporting blog template](#Exporting-blog-template)

<a id="Exporting-blog-layout"></a>
# Exporting blog layout
Blog layout consists of assets(css), blog index, website index, images dir, _blogger_templates, blog directory to quickly set you up with a up and running site. You can customize this css as you like and indexes considering some procedure described [here](customizing.md).
```
blogger export -b <blogname> blog_layout
```
You can  specify a custom folder using -o option. It is relative from blog root folder. However, you can also specify other folder using absolute path from begining.
```
blogger export -b <blogname> blog_layout -o test/
blogger export -b <blogname> blog_layout -o ~/my_website_folder/test/
```

<a id="Exporting-blog-index"></a>
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

<a id="Exporting-blog-assets"></a>
# Exporting blog assets
If you just want blog assets (css, js, fonts). For default support export them inside assets/ folder
```
blogger export -b <blogname> blog_assets -o assets/
```
> If you export css, js in different folder you have to override the default templates with new path. More info [here](customizing.md)

The -o option rule is same as exporting blog_template mentioned above.
```
blogger export -b <blogname> blog_assets -o assets/ 
blogger export -b <blogname> blog_assets -o ~/my_website/assets/
```

<a id="Exporting-blog-configurations"></a>
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
> You cannot specify filename with -o option. blogger export ... -o ~/my_blog.cfg will
create a folder named my_blog.cfg instead. So just user -o ~/ and rename later.

You can import these blog's configuration using config command. see [here](blog_management.md#importing-blog-config)

If you want config of all blogs. copy ~/.blogger/blog_config.cfg to your folder.

<a id="Exporting-blog-template"></a>
# Exporting blog template
Blog template consists of all the snippets that get added to your blog posts during conversion. You can customize default and add other templates. For info to customize look [here](customizing.md)

```
blogger export -b <blogname> blog_template -o _blogger_templates/
```
A _blogger_templates folder will appear in your blog's root directory.
You can specify a custom folder using -o option. It is relative from blog root folder however, you can also specify other folder using absolute path from the beginning.

```
blogger export -b <blogname> blog_template -o test/
blogger export -b <blogname> blog_template -o ~/my_website_folder/test/
```
