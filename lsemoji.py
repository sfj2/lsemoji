#!/usr/bin/python
# -*- coding: utf-8 -*-

# sort by folder
# case-insensitive sorting
# emojis


# todo:
# ignore hidden files

import sys
import os
import math
import getopt

IGNORED = ['.', '..', '.DS_Store']
PACKAGES = ['.prefPane', '.framework', '.app']

path = os.getcwd()

map = {
  # audio
  '.m4a' : "🎵",
  '.wav' : "🎵",
  # video
  '.mpeg' : "📹",
  # documents:
  '.png' : "🎑",
  '.gif' : "",
  '.psd' : "",
  '.doc' : "📝",
  '.docx' : "📝",
  '.ichat' : "💬",
  # text 
  '.txt' : "📄",
  '.eml' : "📫",
  '.ics' : "📅",
  '.html' : "🌏",
  '.htm' : "🌏",
  '.md' : "📝",
  '.rss' : "📰",
  '.vcf' : "👤",

  # misc
  '.url' : "🔗",
  '.webloc' : "🔗",
  
  'package' : "📦"
}


def sizeof_fmt(num):
    """Human friendly file size"""
    unit_list = zip(['bytes', 'kB', 'MB', 'GB', 'TB', 'PB'], [0, 0, 1, 2, 2, 2])
    if num > 1:
        exponent = min(int(math.log(num, 1024)), len(unit_list) - 1)
        quotient = float(num) / 1024**exponent
        unit, num_decimals = unit_list[exponent]
        format_string = '{:.%sf} {}' % (num_decimals)
        return format_string.format(quotient, unit)
    elif num == 0:
        return '0 bytes'
    return '1 byte'

def filterContents(list):

  l = []
  for i in list:
    if i in IGNORED:
      pass
    else:
      l.append(list)
  return l

# class bcolors:
#     HEADER = '\033[95m'
#     OKBLUE = '\033[94m'
#     OKGREY = '\033[1;30m'
#     OKGREEN = '\033[92m'
#     WARNING = '\033[93m'
#     FAIL = '\033[91m'
#     ENDC = '\033[0m'
# 
#     def disable(self):
#         self.HEADER = ''
#         self.OKBLUE = ''
#         self.OKGREEN = ''
#         self.WARNING = ''
#         self.FAIL = ''
#         self.ENDC = ''


try:
  opts, args = getopt.getopt(sys.argv[1:], 'al')
except getopt.GetoptError:
  print 'incorrect usage'
  sys.exit(2)


showHidden = False
showSize = False

for opt, arg in opts:
  if opt == '-a':
    showHidden = True
  elif opt == '-l':
    showSize = True

if len(args) != 0:
  path = os.path.join(path, args[0])

dot = []
dirs = []
files = []



if not os.path.isdir(path):
  if os.path.exists(path):
    files.append(os.path.basename(path))
else:
  for line in os.listdir(path):
    line = line.rstrip()
    if line in IGNORED:
      continue
    elif line[0] == '.' and not showHidden:
      continue

    full = os.path.abspath(os.path.join(path, line))
    if os.path.isdir(full):
      dirs.append(line)
    elif os.path.exists(full):
      files.append(line)

for file in dot:
  if file in IGNORED:
    continue

dirs = sorted(dirs, key=lambda s: s.lower())
home = os.getenv('HOME')

longest = 0
for i in dirs + dot + files:
  l = len(i)
  if (l > longest):
    longest = l

i = 0 
for dir in dirs:

  full = os.path.abspath(os.path.join(path, dir))
  contents = len(filterContents(os.listdir(full)))
  name, extension = os.path.splitext(full)

  emoji = " "
  if full == home:
    emoji = "🏡"
  elif extension in PACKAGES:
    emoji = map['package']
  else:
    emoji = contents == 0 and "📁" or "📂"
 
  if showSize and contents:
    contents = ((longest - len(dir)) * ' ') + (contents > 0 and str(contents) + " item" + (contents > 1 and "s" or ""))
  else:
    contents = ''
 
  print emoji + "  " + dir + "  " + contents
  i += 1

files = sorted(files, key=lambda s: s.lower())
last = None
i = 0

for file in files:

  full = os.path.abspath(os.path.join(path, file))
  name, extension = os.path.splitext(full)

  size = showSize and "  " + ((longest - len(file)) * ' ') + sizeof_fmt(os.path.getsize(full)) or ""

  emoji = map.has_key(extension) and map[extension] or "📄"
  print emoji + "  " + file + size
  i += 1
