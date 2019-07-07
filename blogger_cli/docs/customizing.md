# Customizing templates and design

## Contents
1. [Customizing css](#Customizing-css)
2. [Customizing templates](#Customizing-templates)
    i. [Adding new snippets / templates](#Adding-new-snippets-/-templates)
    ii. [Overriding existing templates](#Overriding-existing-templates)
    iii. [indexes](#indexes)
3. [Dynamic templating](#Dynamic-templating)

## Customizing css
You can customize the default css by simply going to css folder in your blog folder and changing it. Yeah that's it. For adding new css, fonts, js files see below in adding snippets.

## Customizing templates
templates are code snippets that are inserted to the html while converting your files.. eg disqus.html and google_analytics.html are template files that store respective snippets.
For Customizing templates you need a dedicated folder. You can name it whatever and store it wherever you want. Although it is recommended to make a folder inside your blog folder. Anyway just run ```blogger setupblog <blogname>``` and add the path of this folder in templates_dir 's value

> If you have exported blog_templates previously you may have noticed a \_blogger\_templates folder with some inbuilt templates which is for this purpose.

BUILTIN/ AVAILABLE/ RESERVED snippets
- layout.html [meta & snippets]
- light_theme.html [meta]
- dark_theme.html [meta]
- disqus.html [meta]
- google_analytics.html [meta]
- js.html [meta]
- css.html [meta]
- navbar.html [meta]
- navbar-data.html [meta]
- mathjax.html [meta]
- li_tag.html [meta]
- main_index.html
- blog_index.html



### Adding new snippets / templates
First export the blog_template in a test folder
```
blogger export blog_template -o ~/test/
```
Then cd to that folder and go into \_blogger\_templates folder and copy everything to your custom folder.
> This is only required for first time. Once you get layout.html you're done.

Now just create any files with .html extension in your custom templates folder. Then update the 'layout.html' file. Suppose you create footer.html snippet then you open the layout.html and place {{ snippet.footer }} before closing body tag or wherever you want to add this snippet.

NOTE: YOU CANNOT NAME YOUR HTML FILE WITH THE BUILT-IN NAMES LISTED ABOVE.

### Overriding existing templates
You can name your file once of the BUILT_IN names to override it. The most obvious is namvbar_data.html. Here is what the default looks like:
```{
    "Home": "../index.html",
    "Blog": "index.html",
    "Projects": "../projects.html/"
}
```
You can add more navlinks or remove existing BUT make sure everything is inside DOUBLE QUOTES (\") and not single quotes.
Another sensible option is to override layout.html as you have read this in [here](#Adding-new-snippets-/-templates). You can add snippets you want by using {{ snippet_name }} at anywhre you want!

Another one you may want to replace is light\_theme.html you can adjust it according to your preferences.

### indexes
To make your indexes compatible. You just need to wrap your blog's post lists in a div with class 'posts_list'. Blogger reads this div by default. However you can control hat div class should blogger lookup by setting 'index\_div\_name' to your div class name.

To modify what happens when each file is added to index you have to modify li\_tag.html Here is the default contents.
```
<li><a href="{{ snippet.link }}">{{ snippet.title }}</a> </li>
```
You have meta variable access so you can set date in your post meta and reference it by meta.date here. 
```
<li><a href="{{ snippet.link }}">{{ snippet.title }}</a> ({{ meta.date }}) </li>
```

## Dynamic templating
You can access meta class from any custom templates and inbuilt templates. Just add something in your meta and reference it with    {{ meta.var }}
eg I write a md file

test.md
```
<!--
topic: python
date: 3 may
-->
```

Now I can refer it in my template.
```
Date: {{ date }}, topic: {{ python }}
```

Registering new css or js files. Just open css.html file or js.html file in the editor and edit the source. 

Default css.html
```
{% if meta.topic %}
        <link rel="stylesheet" href="../../assets/css/bootstrap.min.css" />
        <link rel="stylesheet" href="../../assets/css/custom.css" />
{% else %}
        <link rel="stylesheet" href="../assets/css/bootstrap.min.css" />
        <link rel="stylesheet" href="../assets/css/custom.css" />
{% endif %}
```
Default js.html
```
<script src="https://code.jquery.com/jquery-3.2.1.min.js" integrity="sha256-hwg4gsxgFZhOsEEamdOYGBf13FyQuiTwlAQgxVSNgt4=" crossorigin="anonymous">
</script>

<script type="text/javascript" src="https://cdn.jsdelivr.net/jquery.jssocials/1.4.0/jssocials.min.js"></script>
<link type="text/css" rel="stylesheet" href="https://cdn.jsdelivr.net/jquery.jssocials/1.4.0/jssocials.css" />
<link type="text/css" rel="stylesheet" href="https://cdn.jsdelivr.net/jquery.jssocials/1.4.0/jssocials-theme-flat.css" />
<link type="text/css" rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" />
```
You can add additional links for new file you make.
