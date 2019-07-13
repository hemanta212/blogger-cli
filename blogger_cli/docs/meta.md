# Meta

## Content
1. [Syntax for meta](#Syntax-for-meta)
2. [Meta for md files ](#Meta-for-md-files )
3. [Meta for ipynb files](#Meta-for-ipynb-files)
4. [Conversion of meta](#Conversion-of-meta)

## Syntax for meta
The default syntax for writing meta is like of html comment ie.
```
<!--
key: value
-->
```
However, this is not forced. You can change the syntax easily by
```
blogger config -b <blogname> meta_format "/* */"
```
will make the syntax something like
```
/*
key: value
*/
```

## Meta for md files
For md files, It is recommended that you write the meta at top of files.
However, technically you can write it wherever you want as far as it is the first occurence of the meta format.

## Meta for ipynb files
For ipynb file meta is lot diverse. You can declare meta in first raw cell.
Your meta will be read then deleted making your notebooks clean. The meta will be written to <filename>.nbdata file where <filename> is the same name as your notebook's name.

Similarly you can make a separate .nbdata file with same name as notebook and blogger will read it during conversion.

Although above is default behaviour you can stop creation of .nbdata files by setting create\_nbdata\_file to false and stop the deletion of meta cell in notebook by delete\_ipynb\_meta to false.
```
blogger config -b <blogname> create_nbdata_file false
blogger config -b <blogname> delete_ipynb_meta false
```
