#!/usr/bin/env python

"shrink photos so that it doesn't take 8 days to transfer them"

from PIL import Image

import os
from   os.path import join, isfile, isdir, dirname, basename

import re
import sys

PIC_RE = re.compile(r'(\.jpe?g$)', re.I)

def shrinkphotos(top, src, dest):
  "shrink each file in top/src/* and save in top/dest/*"
  os.chdir(top)
  src_full, dest_full = [join(top, x) for x in [src, dest]]
  recurse(src_full, dest_full)

def recurse(src, dest):
  "down, down, down"
  if src == dest:
    raise "source and destination directories should not be the same!"

  # os.walk descends by itself and then it's hard to replace src with dest
  # so we recurse manually
  files = os.listdir(src)
  files.sort()
  print " - %s: %d files" % (src, len(files))

  for name in files:
    if isfile(join(src, name)):
      if PIC_RE.search(name):
        # file-shrunk.jpg
        dest_file = join(dest, PIC_RE.sub(r'-shrunk\1', name))
        # skip if already exists
        if not isfile(dest_file):
          if not isdir(dest):
            os.makedirs(dest)
          thumbnail(join(src, name), dest_file)
    elif isdir(join(src, name)):
      recurse(join(src, name), join(dest, name))

def thumbnail(src, dest):
  "shrink src and save to dest"
  img = Image.open(src)
  img.thumbnail((1600, 1200))
  img.save(dest, quality=85)

def shrinkarg(arg):
  "use command line arg as source dir"
  top, src = dirname(arg), basename(arg)
  dest = "%s-shrunk" % src
  shrinkphotos(top, src, dest)

# if dir specified on command line
if len(sys.argv) > 1:
  shrinkarg(sys.argv[1])
  exit(0)

# configuration:
TOP    = '/tmp/pypics'
SOURCE = 'src'
COPY   = 'dest'

shrinkphotos(TOP, SOURCE, COPY)
