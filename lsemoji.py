#!/usr/bin/python
# -*- coding: utf-8 -*-


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
    self.length = 0
    self.unit = ''
    self.owner = ''

    self.modified = self.exists and os.path.getmtime(self.path) or 0

    if self.exists:
      
      self.owner = pwd.getpwuid(os.stat(self.path).st_uid).pw_name
      
      if self.dir:
        list = os.listdir(path)
        for i in list:
          if i != '.' and i != '..':
            self.contents.append(i)

        self.length = len(self.contents)
        self.size, self.unit = str(self.length), 'item' + (len(self.contents) > 1 and 's' or '')

      else:
        self.length = os.path.getsize(self.path)
        self.size, self.unit = self.__size()
        if self.length == 0:
          self.length = 0.00001

  def __str__(self):
    return self.path

  def __size(self):
    """
    Human friendly file size
    """
    num = self.length
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
      return map['.PACKAGE']

    elif self.path.rstrip('/') == os.getenv('HOME'):
      return map['HOME']

    elif self.path == '/':
      return map['ROOT']

    elif os.path.ismount(self.path):
      return map['MOUNT']

    elif os.path.isdir(self.path):
      return len(self.contents) > 0 and map['FOLDER'] or map['FOLDER_EMPTY']

    return map.has_key(extension) and map[extension] or map['DEFAULT']

def emoji(path):
  return File(path).emoji()

if __name__ == '__main__':

  try:
    opts, args = getopt.getopt(sys.argv[1:], 'adfklmrst', ['help'])
  except getopt.GetoptError:
    print 'incorrect usage'
    sys.exit(2)

  if not args:
    args = []

  OPTS = {
    'hidden' :   False, # include hidden files
    'long' :     False, # long output
    'dirs' :     False, # only list directories
    'files' :    False, # only list files
    'reverse' :  False, # reverse sort order
    'merge' :    False, # merge files and directories into one 
    'size' :     False, # sort by size
    'modified' : False, # sort by date modified
    'text' :     False  # text-only output
  }

  for opt, arg in opts:
    if opt == '--help':
      print """🏥  lsemoji [-adfklmrst] [path ...]      

  -a : include hidden files
  -d : only list directories
  -f : only list files
  -k : separate files and directories
  -l : long output
  -m : sort by date modified
  -r : reverse sort order
  -s : sort by size
  -t : ASCII output

   https://github.com/davidfmiller/lsemoji"""
      sys.exit()
    if opt == '-a':
      OPTS['hidden'] = True
    elif opt == '-l':
      OPTS['long'] = True
    elif opt == '-d':
      OPTS['dirs'] = True
    elif opt == '-f':
      OPTS['files'] = True
    elif opt == '-m':
      OPTS['modified'] = True
    elif opt == '-r':
      OPTS['reverse'] = True
    elif opt == '-s':
      OPTS['size'] = True
    elif opt == '-k':
      OPTS['merge'] = True
    elif opt == '-t':
      OPTS['text'] = True


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
        if line[0] == '.' and not OPTS['hidden']:
          continue

        name, extension = os.path.splitext(line)
        f = File(os.path.abspath(os.path.join(path, line)))

        if f.dir and not OPTS['merge']: # and not extension.upper() in PACKAGES:
          dirs.append(f)
        else:
          files.append(f)

    prefix = ''
    t = File(path)
    if len(args) > 1  and (files or dirs) and t.exists and t.dir:
      print t.emoji() + "  " + path
      prefix = '   '
      
    if OPTS['size']:
      sorter = lambda f: f.length
    elif OPTS['modified']:
      sorter = lambda f: f.modified
    else:
      sorter = lambda f: str(f).lower()

    dirs = sorted(dirs, key=sorter, reverse=OPTS['reverse'])
    files = sorted(files, key=sorter, reverse=OPTS['reverse'])

    longest = 0
    biggestSize = '1'
    longestUnit = 0
    
    if OPTS['dirs']:
      files = []
    elif OPTS['files']:
      dirs = []

    for i in dirs + files:
      l = len(os.path.basename(i.path))
      if l > longest:
        longest = l

      if len(i.size) > len(str(biggestSize)):
        biggestSize = i.size

      if len(i.unit) > longestUnit:
        longestUnit = len(i.unit)

    i = 0 

    prevOwner = ''
    for file in dirs + files:

      contents = ''
      if OPTS['long']:
        if file.dir:
          contents = ((longest - len(os.path.basename(file.path))) * ' ') + (int(file.size) > 0 and (((len(biggestSize) - len(file.size)) * ' ') + str(file.size) + ' ' + file.unit  or "") or "")

          if len(file.contents) == 0:
            contents = ' ' * (len(contents) + len(biggestSize) + len(file.unit)) + ' '
          
        elif not file.dir:
          contents = ((longest - len(os.path.basename(file.path))) * ' ') + ((len(biggestSize) - len(file.size)) * ' ') + str(file.size) + ' ' + file.unit

        modified = datetime.fromtimestamp(file.modified)
        contents = contents + ((longestUnit - len(file.unit)) * ' ') + '  ' + str(modified.strftime('%b %d %Y %H:%M')) + '  ' + (file.owner != prevOwner and file.owner or '')

      prevOwner = file.owner

      print (not OPTS['text'] and prefix + file.emoji() + "  " or '') + os.path.basename(file.path) + "  " + contents
      i += 1
