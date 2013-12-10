#!/usr/bin/python
# -*- coding: utf-8 -*-

# sort by folder on or off
# case-insensitive sorting
# emojis
# 


# todo:
# ignore hidden files

import sys
import os
import math
import getopt

IGNORED = ['.', '..', '.DS_Store']
PACKAGES = ['.APP', '.FRAMEWORK', '.PREFPANE', '.SCPTD', '.XCTEST', '.BBPROJECTD']

HOME = os.getenv('HOME')

map = {
  # audio
  '.AIFF' : "🎵",
  '.M4A' : "🎵",
  '.M4R' : "🎵",
  '.MP3' : "🎵",
  '.WAV' : "🎵",

  # video
  '.MPEG' : "🎬",
  '.M4V' : "🎬",

  # books
  '.EPUB' : "📕",

  # images
  '.BMP'  : "🎑",
  '.PNG'  : "🎑",
  '.GIF'  : "🎑",
  '.ICO'  : "🎑",
  '.JPG'  : "🎑",
  '.JPEG' : "🎑",
  '.PSD'  : "🎑",
  '.SVG'  : "🎑",
  '.TIF'  : "🎑",
  '.TIFF' : "🎑",

  # scripts
  '.COFFEE' : "📃",
  '.JS' : "📃",
  '.PL' : "📃",
  '.PY' : "📃",
  '.RB' : "📃",
  '.SCPT' : "🍎",
#  '.SCPTD' : "🍎",
  '.APPLESCRIPT' : "🍎",
  '.SH' : "📃",

  # text 
  '.TXT'  : "📄",
  '.EML'  : "📫",
  '.ICS'  : "📅",
  '.HTML' : "🌏",
  '.HTM'  : "🌏",
  '.MD'   : "📝",
  '.RSS'  : "📰",
  '.VCF'  : "👤",
  '.CSS'  : "🎨",
  '.SCSS'  : "🎨",

  # misc
  '.APP' : "🔧",
  '.DMG' : "💿",
  '.DOC' : "📝",
  '.DOCX' : "📝",
  '.GPX' : "📍",
  '.ICHAT' : "💬",
  '.KML' : "📍",
  '.JAR' : "☕",
  

  '.URL' : "🔗",
  '.WEBLOC' : "🔗",

  '.WEBARCHIVE' : "🌍",

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


def emoji(path):
  """
  Retrieve the emoji icon for a given absolute (full) pathname
  """

  name, extension = os.path.splitext(full)
  extension = extension.upper()

  if extension in PACKAGES:
    return map.has_key(extension) and map[extension] or map['.PACKAGE']

  elif path.rstrip('/') == HOME:
    return "🏡"

  elif os.path.ismount(full):
      return "📀"

  elif os.path.isdir(path):
    return len(filterContents(os.listdir(path))) > 0 and "📂" or "📁"

  return extension in PACKAGES and map['.PACKAGE'] or (map.has_key(extension) and map[extension] or "📄")


def filterContents(list):
  """
  
  """
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
  try:
    path = os.path.join(os.getcwd(), arg)
  except OSError:
    sys.stderr.write('🚫  Unable to determine current directory')
    sys.exit(2)

#  if path in dirs or path in args:
#    continue

  if not os.path.isdir(path):
    if os.path.exists(path):
      files.append(path)
    else:
      sys.stderr.write("🚫  " + arg + " doesn't exist\n")
  else:
    for line in os.listdir(path):
      line = line.rstrip()
      if line in IGNORED:
        continue
      elif line[0] == '.' and not showHidden:
        continue

      name, extension = os.path.splitext(line)
      full = os.path.abspath(os.path.join(path, line))

      if os.path.isdir(full) and not extension.upper() in PACKAGES:
        dirs.append(full)
      elif os.path.exists(full):
        files.append(full)

  prefix = ''
  if len(args) > 1  and (files or dirs) and os.path.isdir(path):
    print emoji(path) + "  " + arg
    prefix = '   '

  dirs = sorted(dirs, key=lambda s: s.lower())

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

    icon = emoji(full)

    if showSize and contents:
      contents = ((longest - len(dir)) * ' ') + (contents > 0 and str(contents) + " item" + (contents > 1 and "s" or ""))
    else:
      contents = ''

    print prefix + icon + "  " + os.path.basename(dir) + "  " + contents
    i += 1

  files = sorted(files, key=lambda s: s.lower())
  last = None
  i = 0

  for file in files:

    full = os.path.abspath(os.path.join(path, file))

    size = showSize and "  " + ((longest - len(file)) * ' ') + sizeof_fmt(os.path.getsize(full)) or ""

    icon = emoji(full)
    print prefix + icon + "  " + os.path.basename(file) + size
    i += 1
