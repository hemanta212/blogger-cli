# Meta

## Content 
1. Syntax for meta
2. Meta for md files 
3. Meta for ipynb files
4. Conversion of meta

## Syntax for meta
The default syntax for writing meta is like of html comment ie.
```
<!--
key: value
-->
```
However, there is no force opinion. You can change the syntax easily by
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
However, technically you can write it whereever you want as far as it is the first occurence of meta syntax.

Meta in md files are not removed by default but you can do so by setting config remove\_md\_meta to true

## Meta for ipynb files
For ipynb file meta is lot diverse. You can declare meta in first markdown cell.
Your meta will be read then deleted making your notebooks clean. The meta will be written to <filename>.nbdata file where <filename> is the same name as your notebook's name.

Similarly you can make a separate .nbdata file with same name as notebook and blogger will read it during conversion.

Although above is default behaviour you can stop creation of .nbdata files by setting create\_nbdata\_file to false and deletion of meta cell in notebook by delete\_ipynb\_meta to false.

## Conversion of meta
