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
import pwd
from datetime import datetime

PACKAGES = ['.APP', '.FRAMEWORK', '.PREFPANE', '.SCPTD', '.XCTEST', '.BBPROJECTD']

#def find_owner(filename):
#    return getpwuid(stat(filename).st_uid).pw_name

map = {
  
  # special
  'HOME' : "🏡",
  'MOUNT' : "📀",
  'FOLDER' : "📂",
  'FOLDER_EMPTY' : "📁",
  'DEFAULT' : "📄",
  'ROOT' : "💻",

  # audio
  '.AIFF' : "🎵",
  '.M4A' : "🎵",
  '.M4R' : "🎵",
  '.MP3' : "🎵",
  '.WAV' : "🎵",
  '.OGG' : "🎵",

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
  '.PDF' : "📝",

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
    self.path = os.path.abspath(path)
    self.exists = os.path.exists(self.path)

    self.dir = self.exists and os.path.isdir(path) or False
    self.contents = []
    self.size = ''
    self.unit = ''
    self.owner = ''

    self.modified = self.exists and os.path.getmtime(self.path) or 0
    
    if self.exists:
      
      self.owner = pwd.getpwuid(os.stat(self.path).st_uid).pw_name
      
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
      if i != '.' and i != '..':
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

    elif self.path == '/':
      return map['ROOT']

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
      path = os.path.abspath(os.path.join(os.getcwd(), arg))
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
        if line[0] == '.' and not showHidden:
          continue

        name, extension = os.path.splitext(line)
        f = File(os.path.abspath(os.path.join(path, line)))

        if f.dir and not extension.upper() in PACKAGES:
          dirs.append(f)
        elif os.path.exists(f.path):
          files.append(f)

    prefix = ''
    t = File(path)
    if len(args) > 1  and (files or dirs) and t.exists and t.dir:
      print t.emoji() + "  " + path
      prefix = '   '

    dirs = sorted(dirs, key=lambda s: str(s).lower())
    files = sorted(files, key=lambda s: str(s).lower())

    longest = 0
    biggestSize = '1'
    longestUnit = 0
    for i in dirs + files:
      l = len(os.path.basename(i.path))
      if l > longest:
        longest = l

      if len(i.size) > len(str(biggestSize)):
        biggestSize = i.size

      if len(i.unit) > longestUnit:
        longestUnit = len(i.unit)

    i = 0 

#    prevOwner = ''
    for file in dirs + files:

      contents = ''
      if showSize:
        if file.dir:
          contents = ((longest - len(os.path.basename(file.path))) * ' ') + (int(file.size) > 0 and (((len(biggestSize) - len(file.size)) * ' ') + str(file.size) + ' ' + file.unit  or "") or "")

          if len(file.contents) == 0:
            contents = ' ' * (len(contents) + len(biggestSize) + len(file.unit)) + ' '
          
        elif not file.dir:
          contents = ((longest - len(os.path.basename(file.path))) * ' ') + ((len(biggestSize) - len(file.size)) * ' ') + str(file.size) + ' ' + file.unit

        when = datetime.fromtimestamp(os.path.getmtime(file.path))
        contents = contents + ((longestUnit - len(file.unit)) * ' ') + '  ' + str(when.strftime('%b %d %Y %H:%M')) + '  ' + file.owner # (file.owner != prevOwner and file.owner or '')
        

      print prefix + file.emoji() + "  " + os.path.basename(file.path) + "  " + contents
      i += 1
#      prevOwner = file.owner
