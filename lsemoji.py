#!/usr/bin/python
# -*- coding: utf-8 -*-

# sort by folder on or off
# case-insensitive sorting
# emojis

"""
Human friendly directory listings
"""

# todo:
# ignore hidden files

import sys
import os
import math
import getopt

IGNORED = ['.', '..', '.DS_Store']
PACKAGES = ['.APP', '.FRAMEWORK', '.PREFPANE', '.SCPTD', '.XCTEST', '.BBPROJECTD']

map = {
  
  # special
  'HOME' : "🏡",
  'MOUNT' : "📀",
  'FOLDER' : "📂",
  'FOLDER_EMPTY' : "📁",
  'DEFAULT' : "📄",

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

class File:
  """
  
  """
  def __init__(self, path):
    """
    
    """
    self.path = path
    self.dir = os.path.isdir(path)
    self.contents = []
    self.size = ''
    self.unit = ''

    if self.dir:
      self.contents = self.__filter(os.listdir(path))
      self.size, self.unit = str(len(self.contents)), 'item' + (len(self.contents) > 1 and 's' or '')
    else:
      self.size, self.unit = self.__size()

  def __str__(self):
    return self.path

  def __filter(self, list):
    """
    
    """
    l = []
    for i in list:
      if i in IGNORED:
        pass
      else:
        l.append(i)
    return l

  def __size(self):
    """
    Human friendly file size
    """
    num = os.path.getsize(self.path)
    unit_list = zip(['bytes', 'kB', 'MB', 'GB', 'TB', 'PB'], [0, 0, 1, 2, 2, 2])

    if num == 1:
      return '1', 'byte'      
    elif num == 0:
      return '0', 'bytes'
    else:
      exponent = min(int(math.log(num, 1024)), len(unit_list) - 1)
      quotient = float(num) / 1024**exponent
      unit, num_decimals = unit_list[exponent]
      format_string = '{:.%sf}' % (num_decimals)
      return format_string.format(quotient), unit


  def __len__(self):
    return len(self.contents)

  def emoji(self):
    """
    Retrieve the emoji icon for a given absolute (full) pathname
    """
    name, extension = os.path.splitext(self.path)
    extension = extension.upper()

    if extension in PACKAGES:
      return map.has_key(extension) and map[extension] or map['.PACKAGE']

    elif self.path.rstrip('/') == os.getenv('HOME'):
      return map['HOME']

    elif os.path.ismount(self.path):
      return map['MOUNT']

    elif os.path.isdir(self.path):
      return len(self.contents) > 0 and map['FOLDER'] or map['FOLDER_EMPTY']

    return map.has_key(extension) and map[extension] or map['DEFAULT']


if __name__ == '__main__':

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

    if not os.path.isdir(path):
      if os.path.exists(path):
        files.append(File(path))
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
        f = File(os.path.abspath(os.path.join(path, line)))

        if f.dir and not extension.upper() in PACKAGES:
          dirs.append(f)
        elif os.path.exists(f.path):
          files.append(f)

    prefix = ''
    if len(args) > 1  and (files or dirs) and f.dir:
      print f.emoji() + "  " + arg
      prefix = '   '

    dirs = sorted(dirs, key=lambda s: str(s).lower())

    longest = 0
    biggestSize = 1
    for i in dirs + files:
      l = len(os.path.basename(i.path))
      if l > longest:
        longest = l

      if len(i.size) > len(str(biggestSize)):
        biggestSize = i.size

    i = 0 

    for dir in dirs:

      contents = ''
      if showSize and len(dir.contents):
        contents = ((longest - len(os.path.basename(dir.path))) * ' ') + (int(dir.size) > 0 and (((len(biggestSize) - len(dir.size)) * ' ') + str(dir.size) + ' ' + dir.unit  or "") or "")

      print prefix + dir.emoji() + "  " + os.path.basename(dir.path) + "  " + contents
      i += 1

    files = sorted(files, key=lambda s: str(s).lower())
    last = None
    i = 0

    for file in files:

      size = showSize and "  " + ((longest - len(os.path.basename(file.path))) * ' ') + ((len(biggestSize) - len(file.size)) * ' ') + str(file.size) + ' ' + file.unit  or ""

      print prefix + file.emoji() + "  " + os.path.basename(file.path) + size
      i += 1
