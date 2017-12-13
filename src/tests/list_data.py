import glob
import os

def listDataDirectory():
    current_file = os.path.realpath(__file__)
    current_dir = os.path.split(current_file)[0]
    data_dir = current_dir + "/data/*"
    return glob.glob(data_dir)
