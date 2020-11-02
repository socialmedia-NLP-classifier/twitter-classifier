import os
import pandas as pd
import time
import pickle
import numpy as np
import platform

def clock(func): # from version 2, page 203 - 205 of Fluent Python by Luciano Ramalho
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - t0
        arg_lst = [] #name = func.__name__
        if args:
            arg_lst.append(', '.join(repr(arg) for arg in args))
        if kwargs:
            pairs = ["%s=%r" % (k,w) for k, w in sorted(kwargs.items())]
            arg_lst.append(", ".join(pairs))
        arg_str = ", ".join(arg_lst)
        print("[%0.8fs] %s(%s) -> %r " % (elapsed, func.__name__, arg_str, result))
        return result
    return clocked

def get_cd():
    """
    uses the os.path function to get the filename and the absolute path to the current directory
    Also does a primative check to see if the path is correct, there has been instances where the CD was different, hence the check.

    return Value(s):
    - scriptPath: the full directory path
    - filePath: the full path that includes the current file
    """
    # Get the path to this file
    scriptPath, filePath = os.path.realpath(__file__), ""
    # get the os name and the backslash or forward slash depending on the OS
    os_name = platform.system()
    path_slash = "/" if os_name in ["Linux", 'Darwin'] else "\\"
    # remove the file name from the end of the path
    for i in range(1,len(scriptPath)+1):
        if scriptPath[-i] == path_slash:
            scriptPath = scriptPath[0:-i]#current path, relative to root direcotory or C drive
            break
    if os.getcwd() != scriptPath: filePath = scriptPath + path_slash
    return scriptPath, filePath

def fullPath(fileName, folder=""):
    """
        given the folder and the file name, it returns a string object that have the type of slash right for the computer's OS

        Parameters:
        - fileName: the name of the file
        - folder: the folder where the file is located in, if it's in the same directory, then use an empty string
    """
    _, filePath = get_cd()
    # we need the os name because different OS uses / or \ to navigate the file system
    osName = platform.system()
    # get the full path to the file that we're trying to open, and depending on the OS, the slashes changes
    fullLocName = filePath + folder + "\\" + fileName
    if osName == "Windows": pass
    else:
        # for OS' like linux and mac(Darwin)
        fullLocName = fullLocName.replace("\\", "/")
    return fullLocName


def mergeData(filenames, col_rename, exportname):
    """
    merge csv files to make a big dataframe and save in byte form
    """
    df = pd.DataFrame
    for filename in filenames:
        current_df = pd.read_csv(filename)

def main():
    filenames = []
    to_merge =[]
    config_loc = fullPath("MERGED_FILES.txt", folder="local_dataset")
    merge_file = fullPath("TO_MERGE.txt", folder="local_dataset")
    try:
        with open(config_loc, "r") as f:
            filenames = f.read().split()
            f.close()
            print(f"found MERGED_FILE.txt, program will ignore merging the following {filenames} ")
    except FileNotFoundError:
        print("no file in dir, creating a MERGE_FILE.txt to store merged files")
        with open(config_loc, "w") as f:
            f.close()


    try:
        with open(merge_file, "r") as f:
            to_merge = f.read().split(";")
            f.close()
            print(f"found TO_MERGE.txt, program will merge the following: {to_merge}")
    except FileNotFoundError:
        with open(merge_file, "w") as f:
            f.close()


    for filename in to_merge:
        if len(filename) > 0:
            name_column = filename.split()

            df = pd.read_csv(fullPath(name_column[0], folder="local_dataset"))
            print(df.head())
            nullCount = df.isnull().sum()
            dupCount = df.duplicated().sum()
            print(f"# of nulls:\n{nullCount}")
            print(f"duplicate entries:\n{dupCount}")
            df.drop_duplicates(inplace=True)






if __name__ == "__main__":
    main()