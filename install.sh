#!/usr/bin/env bash

mkdir -p ~/bin
echo "🌍  Downloading lsemoji install script from https://github.com/davidfmiller/lsemoji..."

curl -fsSl https://raw.github.com/davidfmiller/lsemoji/master/lsemoji.py > ~/bin/lsemoji
chmod +x ~/bin/lsemoji

echo "👍  lsemoji is in ~/bin"

