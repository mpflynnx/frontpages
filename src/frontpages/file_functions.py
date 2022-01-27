import os
import re
import shutil
import tempfile
from datetime import date
from os.path import basename

import pathlib3x as pathlib
from pathlib3x import Path

###################################################
today = date.today()
# YYmmdd
d1 = today.strftime("%Y%m%d")

string = d1 + "-"

###################################################


def rename_all4(myfile, string):
    """
    Append 'string' to filename 'myfile'.
    """

    if Path.is_file(myfile):
        new = myfile.name + string  # create new filename
        dest = myfile.parent.absolute() / new  # create new full path with new filename
        if not dest.exists():
            os.rename(myfile, dest)  # rename src to dest
            print(f"Filename '{myfile.name}' renamed to '{new}'.")
            return
        else:
            print(f"Filename '{dest.name}' already exists, will not rename.")
            return
    return


def match(mylist):
    """
    Return a list of regex matching items from mylist.
    """
    matches = []
    count = 0
    for i in range(len(mylist)):
        regex = re.compile(r"^_12\d{7}.+")
        if re.search(regex, basename(mylist[i])):
            count += 1
            matches.append(mylist[i])
    print("Found " + str(count) + " images.")
    return matches


#  def match2(mylist):
    #  """
    #  Return a list of regex matching items from mylist.
    #  """
    #  matches = []
    #  count = 0
    #  for i in range(len(mylist)):
        #  #  regex = re.compile(r"^_12\d{7}_\w+")
        #  regex = re.compile(r"^_12\d{7}_.+.jpg$") # must end in .jpg
        #  if re.search(regex, basename(mylist[i])):
            #  count += 1
            #  matches.append(mylist[i])
    #  print("Found " + str(count) + " images.")
    #  return matches


def prepend_date(myfiles):
    """Prepend date to 'filenames' in list 'myfiles'."""

    today = date.today()
    # YYmmdd
    d1 = today.strftime("%Y%m%d")

    regex = r"^[0-9]{8}-"

    for i in range(len(myfiles)):
        # check if the file exist or not
        if Path.is_file(myfiles[i]):
            src = myfiles[i]  # get source full path incl filename
            #  fdir = myfiles[i].parent.absolute()  # get just the path no filename
            if not re.match(regex, src.name):
                new = d1 + "-" + src.name  # create new filename
                dest = (
                    src.parent.absolute() / new
                )  # create new full path with new filename
                if not dest.exists():
                    os.rename(src, dest)  # rename src to dest
                    print(f"Filename '{src.name}' renamed to '{new}'.")
                else:
                    print(f"Filename '{dest.name}' already exists, will not rename.")
                    continue
            else:
                print(f"Filename '{src.name}' already prepended, will not rename.")
                continue

        else:
            print(f"Filename '{src.name}' missing, cannot rename.")
            continue


def rename_all2(myfiles):
    """
    Rename any files in list 'myfiles',
    if the filename matches the regular expression 'regex'.
    """
    regex = r"^_[0-9]{9}_"

    for i in range(len(myfiles)):
        # check if the file exist or not
        if Path.is_file(myfiles[i]):
            src = myfiles[i]  # get source full path incl filename
            if re.match(regex, src.name):
                new = src.name[11:]  # create new filename
                dest = (
                    src.parent.absolute() / new
                )  # create new full path with new filename
                if not dest.exists():
                    os.rename(src, dest)  # rename src to dest
                    print(f"Filename '{src.name}' renamed to '{new}'.")
                else:
                    print(f"Filename '{dest.name}' already exists, will not rename.")
                    continue
            else:
                print(f"Filename '{src.name}' doesn't match pattern, will not rename.")
                continue

        else:
            print(f"Filename '{src.name}' missing, cannot rename.")
            continue


def files_list(mydir):
    """Create a list of filenames in mydir."""

    searchDir = Path(mydir)
    myfiles = list(searchDir.iterdir())
    return myfiles


def create_tmp():
    """
    Creates something like this '/tmp/tmpdyt9dmlq'
    """
    return Path(tempfile.mkdtemp())


def delete_tmp(tmp):
    """ """
    shutil.rmtree(tmp, ignore_errors=True)


def check_filename(myfiles, string):
    """
    Check filesnames in 'mylist' for files starting with 'string'.
    """
    regex = r"^" + re.escape(string)

    for i in range(len(myfiles)):
        if Path.is_file(myfiles[i]):
            src = myfiles[i]  # get source full path incl filename
            if re.match(regex, src.name):
                return True
    return False


def move_files(abspath, dest, ext):
    """
    Move all files with extension 'ext' in absolute path 'abspath'
    to absolute destination path, 'dest'.
    """

    newtmp = Path(abspath)
    movelist = sorted(newtmp.rglob(f"*.{ext}"))

    for i in range(len(movelist)):
        shutil.move(movelist[i], dest / movelist[i].name)
