# lsemoji

Human-friendly directory listings in your terminal. Example usage:

    ~/Documents/git/lsemoji/files> lsemoji .
    📂  dir  
    📁  empty  
    📦  App.app
    🍎  apple.scpt
    📦  apple.scptd
    📦  archive.zip
    🎵  audio.m4a
    🎵  audio.wav
    📅  calendar.ics
    💬  chat.ichat
    👤  contact.vcf
    📄  document.pdf
    📫  email.eml
    🎑  icon.ico
    🎑  image.png
    🎑  image.svg
    🎑  image.tif
    📃  javascript.js
    🔗  link.webloc
    📍  map.gpx
    📝  markdown.md
    📰  news.rss
    🌏  page.htm
    🌏  page.html
    🌍  page.webarchive
    🎨  styles.css
    🎨  styles.scss
    📄  text.txt
    🎬  video.mpeg
    📝  word.doc
    📝  word.docx

## Usage

    > lsemoji [path ...]

Use the `--help` option for an explanation of all options/arguments.

## Install
    curl -fsSl https://raw.github.com/davidfmiller/lsemoji/master/install.sh | sh
    export PATH="$PATH:~/bin"

You might want to create an alias for it, too. For bash do the following in your .profile:

    function __emoji () { python ~/Documents/git/lsemoji/lsemoji.py "$@"; } 
    alias l="__emoji"

## Python module

`lsemoji` is also built to be a reusable Python module: 

    > python 
    ...
    >>> import lsemoji as ls
    >>> print ls.emoji('/')
    💻 

## TODO

- [https://github.com/xattr/xattr](https://github.com/xattr/xattr)
-  Unicode funk

    📂  Roy Orbison                                       1 item   777  Mar 08 2012 10:49            
    📂  Röyksopp                                        1 item   777              11:38            
    📂  Rufus Wainwright                                  7 items  777  May 31 2012 10:30   
