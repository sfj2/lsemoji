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
    
## Install

Clone the repo (or just save the .py file locally) and ensure the script is in your path:

    export PATH="$PATH:~/bin"

You might want to create an alias for it, too. For bash do the following in your .profile:

    function __emoji () { python ~/Documents/git/lsemoji/lsemoji.py "$@"; } 
    alias l="__emoji"
