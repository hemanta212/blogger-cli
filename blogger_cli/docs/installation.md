# Installation Guide
This document inclues:
- [Installing methods](#Installing-methods)
- [Updating blogger_cli](#Updating-blogger_cli)
- [Uninstalling blogger_cli](#Uninstalling-blogger_cli)
- [Developing guide](#Developing-guide)

## Custom installer
```
curl -sSL https://raw.githubusercontent.com/hemanta212/blogger-cli//master/get_blogger.py
```

## WHY
The custom installer provides a isolated installation for blogger-cli. It is very desirable since blogger-cli relies on nbconvert / jupyter-core that have many dependencies and are likely to cause you some trouble.
Even if you install it in virutalenv yourself you need ot constantly activate it in order to use it. This installer does exactly that and in addition puts blogger command in the system's path.

## With pip
```
pip install blogger-cli
```
If you already have jupyter in your system python then a pip install will work just fine and you can access blogger without any hassle.


# Updating blogger_cli
If you have installed through custom installation then,
```
blogger update
```
See blogger update --help for information regaurding various options

**For pip installations**:
```
pip install --upgrade blogger-cli
```


# Uninstalling blogger_cli
```
blogger uninstall
```
If you have installed from custom installer

```
pip uninstall blogger-cli
```
If you have installed through pip

## Developing guide
Clone the repository using,
```
$ git clone https://github.com/hemanta212/blogger-cli
```
change working directory into the blogger-cli folder
```
$ cd blogger-cli
```
Then install it in development mode using pip
```
pip install -e .
```
