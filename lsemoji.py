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
PACKAGES = ['.PREFPANE', '.FRAMEWORK', '.APP', '.XCTEST']

map = {
  # audio
  '.M4A' : "🎵",
  '.M4R' : "🎵",
  '.WAV' : "🎵",
  '.MP3' : "🎵",
  '.AIFF' : "🎵",

  # video
  '.MPEG' : "🎬",
  '.M4V' : "🎬",

  # books
  '.EPUB' : "📕",

  # images
  '.BMP' : "🎨",
  '.PNG' : "🎨",
  '.GIF' : "🎨",
  '.JPG' : "🎨",
  '.JPEG' : "🎨",
  '.TIF' : "🎨",
  '.TIFF' : "🎨",
  '.ICO' : "🎨",
  '.SVG' : "🎨",
  '.PSD' : "🎨",
  '.DOC' : "📝",
  '.DOCX' : "📝",
  '.ICHAT' : "💬",

  # scripts
  '.SCPT' : "📃",
  '.SH' : "📃",
  '.PY' : "📃",
  '.PL' : "📃",

  # text 
  '.TXT' : "📄",
  '.EML' : "📫",
  '.ICS' : "📅",
  '.HTML' : "🌏",
  '.HTM' : "🌏",
  '.MD' : "📝",
  '.RSS' : "📰",
  '.VCF' : "👤",


  # misc
  '.GPX' : "📍",
  '.KML' : "📍",
  '.URL' : "🔗",
  '.WEBLOC' : "🔗",
  '.DMG' : "💿",
  '.APP' : "🔧",

  '.PKG' : "📦",
  '.ZIP' : "📦",
  '.GZ' : "📦",
  
  
   # defaults
  '.PACKAGE' : "📦",
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

try:
  opts, args = getopt.getopt(sys.argv[1:], 'al')
except getopt.GetoptError:
  print 'incorrect usage'
  sys.exit(2)

if not args:
  args = []

showHidden = False
showSize = False

for opt, arg in opts:
  if opt == '-a':
    showHidden = True
  elif opt == '-l':
    showSize = True

if len(args) == 0:
  args.append('')

dirIndex = -1

for arg in args:

  dirs = []
  files = []

  dirIndex += 1
  path = os.path.join(os.getcwd(), arg)

#  if path in dirs or path in args:
#    continue

  if not os.path.isdir(path):
    if os.path.exists(path):
      files.append(path)
  else:
    for line in os.listdir(path):
      line = line.rstrip()
      if line in IGNORED:
        continue
      elif line[0] == '.' and not showHidden:
        continue

      full = os.path.abspath(os.path.join(path, line))
      if os.path.isdir(full):
        dirs.append(full)
      elif os.path.exists(full):
        files.append(full)

  prefix = ''
  if len(args) > 1  and (files or dirs) and os.path.isdir(path):
    print (dirIndex > 0 and "" or '') + "📁  " + arg
    prefix = '   '

  dirs = sorted(dirs, key=lambda s: s.lower())
  home = os.getenv('HOME')

  longest = 0
  for i in dirs + files:
    l = len(i)
    if (l > longest):
      longest = l

  i = 0 
  biggest = ''
  for dir in dirs:

    full = os.path.abspath(os.path.join(path, dir))
    contents = len(filterContents(os.listdir(full)))
    name, extension = os.path.splitext(full)

    if len(str(contents)) > biggest:
      biggest = len(str(contents))

    extension = extension.upper()

    emoji = " "
    if full == home:
      emoji = "🏡"
    elif extension in PACKAGES:
      emoji = map.has_key(extension) and map[extension] or map['.PACKAGE']
    else:
      emoji = contents == 0 and "📁" or "📂"

    if showSize and contents:
      contents = ((longest - len(dir)) * ' ') + (contents > 0 and str(contents) + " item" + (contents > 1 and "s" or ""))
    else:
      contents = ''

    print prefix + emoji + "  " + os.path.basename(dir) + "  " + contents
    i += 1

  files = sorted(files, key=lambda s: s.lower())
  last = None
  i = 0

  for file in files:

    full = os.path.abspath(os.path.join(path, file))
    name, extension = os.path.splitext(full)

    extension = extension.upper()

    size = showSize and "  " + ((longest - len(file)) * ' ') + sizeof_fmt(os.path.getsize(full)) or ""

    emoji = map.has_key(extension) and map[extension] or "📄"
    print prefix + emoji + "  " + os.path.basename(file) + size
    i += 1
