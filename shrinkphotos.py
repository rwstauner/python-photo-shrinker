#!/usr/bin/env python

"shrink photos so that it doesn't take 8 days to transfer them"

# Copyright (c) 2012 Randy Stauner
# Licensed under the MIT License: http://opensource.org/licenses/MIT

from PIL import Image

import os
from   os.path import join, isfile, isdir, dirname, basename

import re
import sys

# configuration

DIR_SUFFIX  = '-shrunk'
FILE_SUFFIX = '-shrunk'
# PIC_RE should capture the file extension;
# Later FILE_SUFFIX will be inserted before it
PIC_RE      = re.compile(r'(\.jpe?g)$', re.I)
QUALITY     = 85
RESOLUTION  = (1600, 1200)


def shrinkphotos(top, src, dest):
  "shrink each file in top/src/* and save in top/dest/*"
  os.chdir(top)
  src_full, dest_full = [join(top, x) for x in [src, dest]]

  print "shrinking images found in\n  %s\nand saving to\n  %s" % \
    (src_full, dest_full)

  # Just a warning; Allow the script to be re-run.
  if isdir(dest_full):
    print "destination %s already exists" % (dest_full)

  if raw_input("\ncontinue? (y/n): ").lower() == 'y':
    recurse(src_full, dest_full)


def recurse(src, dest):
  "down, down, down"

  # I suppose this could be allowed as long as there is a FILE_SUFFIX
  if src == dest:
    raise "source and destination directories should not be the same!"

  # os.walk descends by itself and then it's hard to replace src with dest
  # so we recurse manually
  files = os.listdir(src)
  files.sort()
  print " - %s: %d files" % (src, len(files))

  for name in files:
    if isfile(join(src, name)):
      # If the file name matches the re (has the right extension)
      if PIC_RE.search(name):
        # src/file.jpg => dest/file-shrunk.jpg
        dest_file = join(dest, PIC_RE.sub(r'%s\1' % FILE_SUFFIX, name))
        # skip if already exists
        if not isfile(dest_file):
          # Ensure destination directory exists
          if not isdir(dest):
            os.makedirs(dest)
          thumbnail(join(src, name), dest_file)
    # descend to the next directory
    elif isdir(join(src, name)):
      recurse(join(src, name), join(dest, name))


def thumbnail(src, dest):
  "shrink src and save to dest"
  img = Image.open(src)
  # Ensure image is not larger than RESOLUTION.
  img.thumbnail(RESOLUTION)
  # Set compression level on the new image.
  img.save(dest, quality=QUALITY)


def shrinkarg(arg):
  "use command line arg as source dir"

  if arg == '' or arg == '.':
    arg = os.getcwd()
  # Strip trailing slash, etc
  arg = os.path.normpath(arg)

  top, src = dirname(arg), basename(arg)
  dest = "%s%s" % (src, DIR_SUFFIX)

  shrinkphotos(top, src, dest)


if __name__ == "__main__":
  # If a directory is specified on command line
  if len(sys.argv) > 1:
    shrinkarg(sys.argv[1])
  # Else use the directory the script is in
  else:
    shrinkarg(dirname(sys.argv[0]))
