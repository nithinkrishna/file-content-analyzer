from os import listdir, mkdir, rename
from os.path import isfile, join, isdir
from shutil import copyfile, rmtree, move

import sys, time

from random import choice
from string import ascii_uppercase

PATH = sys.argv[1]

def listFolders(path):
  return filter(lambda f: isdir(join(path, f)), listdir(path))

def initTypeDir(path):
  if not isdir(path):
    mkdir(path)

def processType(tp, sourcePath):
  print "-- STARTED -- {0}".format(sourcePath)
  destPath = join(PATH, tp)
  initTypeDir(destPath)

  sFolders = listFolders(sourcePath)

  # All elements except the last
  for sFolder in sFolders:
    fromFolder = join(sourcePath, sFolder)
    rand = ''.join(choice(ascii_uppercase) for i in range(5))
    toFolder = join(destPath, "{0}-{1}".format(rand, time.time()))
    mkdir(toFolder)
    rename(fromFolder, toFolder)

  print "-- COMPLETED -- {0}".format(sourcePath)

def processDir(dPath):
  print "-- STARTED -- {0}".format(dPath)
  for tp in listdir(dPath):
    tPath = join(dPath, tp)
    processType(tp, tPath)
  rmtree(dPath)
  print "-- COMPLETED -- {0}".format(dPath)

for klass in listFolders(PATH):
  d = join(PATH, klass)
  processDir(d)
