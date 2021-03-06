from os import listdir, mkdir
from os.path import isfile, join, isdir
from shutil import copyfile
from tika import detector
from shutil import move

import ntpath
import re
import sys
import time

import sys, traceback
from file_count import *

# Log path
log = open(sys.argv[3], "a")

def safeMakeDir(path):
  if not isdir(path):
    mkdir(path)

def saveFile(folder, fileName, tmpPath):
  countH = FileCountHandler(folder)
  subFolder = int(countH.readCount() / 100) + 1
  safeMakeDir(join(folder, str(subFolder)))
  fPath = join(folder, str(subFolder), fileName)
  move(tmpPath, fPath)
  countH.incrementCount()
  log.write("{0}\n".format(fPath))

def fetchFile(path, END_POINT):
  fileName = "{0}-{1}".format(ntpath.basename(path), time.time())

  # Download File
  tmpPath = join(END_POINT, fileName)
  copyfile(path, tmpPath)

  # Run Tika
  tp = detector.from_file(path).replace("/", "-")

  d = join(END_POINT, tp)

  safeMakeDir(d)

  saveFile(d, fileName, tmpPath)


def dfs_traversal(path, END_POINT):
  if isfile(path):
    fetchFile(path, END_POINT)
    return

  for f in listdir(path):
    try:
      dfs_traversal(join(path, f), END_POINT)
    except Exception as e:
      log.write( "******** ERROR while processing ******** {0}\n".format(path)      )
      log.write( "******** ERROR while processing ******** {0}\n".format(e.args) )
      log.write( "******** ERROR while processing ******** {0}\n".format(e)      )
      traceback.print_exc(file=log)

if __name__ == '__main__':
  MOUNT_POINT = sys.argv[1]
  END_POINT = sys.argv[2]

  dfs_traversal(MOUNT_POINT, END_POINT)
