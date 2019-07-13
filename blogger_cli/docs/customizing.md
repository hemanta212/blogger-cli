# Customizing templates and design

## Contents
1. [Customizing css](#Customizing-css)
2. [Customizing templates](#Customizing-templates)
    - [Adding new snippets / templates](#Adding-new-snippets--templates)
    - [Overriding existing templates](#Overriding-existing-templates)
    - [indexes](#indexes)
3. [Dynamic templating](#Dynamic-templating)

## Customizing css
You can customize the default css by simply going to css folder in your blog folder and changing it. Yeah that's it. For adding new css, fonts, js files see below in adding snippets. Look [here](#adding-static-files) for adding new.

## Customizing templates
Templates are code snippets that are inserted to the html while converting your files.. eg disqus.html and google_analytics.html are template files that store respective snippets.

First export all templates to your blog's root dir
```
blogger export blog_template
```
or specify other folder using -o option. A \_blogger\_templates folder should appear.

Now add this folder's full path to your blog's config
```
blogger config -b <blogname> templates_dir /path/to/dir
```

Every templates except layout.html are small building blocks(snippets) and layout.html is the collector that arrange this snippets. #

## Adding new snippets / templates
To add a new snippet, just create any files with .html extension in the templates folder. Then update the 'layout.html' file.

Suppose you create footer.html snippet then you open the layout.html and place {{ snippet.footer }} before closing body tag or wherever you want to add this snippet.

### Overriding existing templates
You are free to edit the default templates and changes will be reflected. However if you mess up you can always again export blog_template from above process.

You may want to eddit navbar_data.html. Here is what the default looks like:
```{
    "Home": "../index.html",
    "Blog": "index.html",
    "Projects": "../projects.html/"
}
```
You can add more navlinks or remove existing BUT make sure everything is inside DOUBLE QUOTES (\") and not single quotes and do not put comma in the end of last item.

It is also a googd idea to override layout.html as you have read this in [here](#Adding-new-snippets--templates). You can add snippets you want by using {{ snippet_name }} at anywhre you want!


### indexes
To make your indexes compatible. You just need to wrap your blog's post lists in a div with class 'posts_list'. Blogger reads this div by default. However you can control hat div class should blogger lookup by setting 'index\_div\_name' to your div class name.
```
blogger config -b <blogname> index_div_name posts
```
Now blogger will look for div with class 'posts' instead!

To modify what happens when each file is added to index you have to modify li\_tag.html template. Here is the default content.
```
<li><a href="{{ snippet.link }}">{{ snippet.title }}</a> </li>
```
You have meta variable access so you can set date in your post meta and reference it by meta.date here.
```
<li><a href="{{ snippet.link }}">{{ snippet.title }}</a> ({{ meta.date }}) </li>
```

## Dynamic templating
You can have logics and variables in the blog_templates for dynamic template generation.

### Syntax
1. Variables
The variables are referenced using {{ var }} syntax.

2. Logic code
Logic code are written inside {% %} brackets. Well basic logic like if statements, for loop, while loop etc are available.
eg: if else
```
{% if var %}
    something
{% elif %}
    sth
{% else %}
    sth
{% endif %}
```
for loop
```
{% for i in var %}
    something
{% endfor %}

{% for i,j in zip(var.a,var.b) %}
{% endfor %}
```

#### Usage
You can execute any python codes and use logic anyway you like inside {% %} in any templates.
You have 2 variable access.
* snippet : This is only available in layout.html through this you can access any other snippet file's content along with title and file link.

* meta: Meta is available in every template. You write the meta in your post and use it in the template. Its entirely your implementation. More info on meta is [here](meta.md)

* config: You may see config variable used in some templates eg disqus.html it just make disqus_username and google analytics id accessible for templating and IT IS NOT AVAILABLE in other templates except disqus.html and google_analytics.html

> You can access meta class from any custom templates and inbuilt templates. Just add something in your meta and reference it with {{ meta.var }}

eg I write a md file
test.md
```
<!--
topic: python
date: 3 may
-->
```

Now I can refer it in templates.
```
Date: {{ meta.date }}, topic: {{ meta.topic }}
```

#### Adding static files
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
