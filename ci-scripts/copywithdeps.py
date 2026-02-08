#!/usr/bin/python
# Python 3 compatible copywithdeps.py (fixes xreadlines removed in Python 3)
# From google/brailleback, with for line in f.xreadlines() -> for line in f

from __future__ import print_function
import fnmatch
import getopt
import os.path
import re
import shutil
import sys

ASSIGN_RE = re.compile(r"\s*assign\s+([^# ]+)(\s+([^# ]+))?")
SUBST_RE = re.compile(r"\\\{([a-zA-Z0-9]+)\}")
INCLUDE_RE = re.compile(r"^\s*include\s+([^# ]+)")


def main():
  try:
    opts, args = getopt.getopt(sys.argv[1:], "nX:",
                               ["dry-run", "exclude="])
  except getopt.GetoptError as msg:
    Usage(msg)
  dryrun = False
  excluded = []
  for opt, val in opts:
    if opt in ("-n", "--dry-run"):
      dryrun = True
    if opt in ("-X", "--exclude"):
      excluded.append(val)
  if len(args) < 3:
    Usage("too few arguments")
  destdir = args[-1]
  if not os.path.isdir(destdir):
    Die("Not a directory: " + destdir)

  tocopy = set()
  for filename in args[:-1]:
    if MatchesAny(os.path.basename(filename), excluded):
      print("Skipping:", filename)
      continue
    tocopy.add(filename)
    tocopy.update(GetDeps(filename))
  for filename in tocopy:
    print("Copying:", filename)
    if not dryrun:
      shutil.copy(filename, destdir)


def Die(why):
  print(why, file=sys.stderr)
  sys.exit(1)


def Usage(msg=None):
  usage = ("Usage: %s [-n | --dry-run] [-X | --exclude=GLOB] FILE... DESTDIR" %
           sys.argv[0])
  if msg:
    Die("%s\n\n%s" % (msg, usage))
  else:
    Die(usage)


def GetDeps(filename, assigns=None):
  result = []
  if assigns is None:
    assigns = dict()
  else:
    assigns = dict(assigns)
  directory = os.path.dirname(filename)
  with open(filename, "r", encoding="utf-8", errors="replace") as f:
    for line in f:
      line = Substitute(assigns, line.rstrip(), filename)
      m = ASSIGN_RE.match(line)
      if m:
        name = m.group(1)
        value = m.group(3)
        if value:
          assigns[name] = value
        else:
          del assigns[name]
      m = INCLUDE_RE.match(line)
      if m:
        name = os.path.join(directory, m.group(1))
        result.append(name)
        result.extend(GetDeps(name, assigns))
  return result


def MatchesAny(filename, globs):
  for glob in globs:
    if fnmatch.fnmatch(filename, glob):
      return True
  return False


def Substitute(assigns, line, filename):
  while True:
    m = SUBST_RE.search(line)
    if not m:
      return line
    try:
      value = assigns[m.group(1)]
    except KeyError:
      Die("Undefined substitution on line: %s in file %s" % (line, filename))
    line = line[0:m.start(0)] + value + line[m.end(0):]


if __name__ == "__main__":
  main()
