#!/usr/bin/env bash

mkdir -p ~/bin
echo -e "\033[1;34mDownloading shell script ...\033[0m"

curl –silent https://raw.github.com/davidfmiller/lsemoji/master/lsemoji.py > ~/bin/lsemoji > /dev/null 2>&1
chmod +x ~/bin/lsemoji

echo -e "\033[1;32mDone!\033[0m"
echo -e "\033[1;33mMake sure ~/bin is in your PATH to have lsemoji available\033[0m"
