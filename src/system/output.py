import os

def preventOverwrite(filename,prefix=False,create_file=True):
    """
    checks to see if a file or directory already exists and creates a new filename
    if it does. It can also create the file if specificed
    """
    basefilename,extension = os.path.splitext(filename)
    out_filename = filename
    file_exists = os.path.exists(out_filename)
    num = 1
    while file_exists:
        out_filename =  basefilename + "({0})".format(num) + extension
        file_exists = os.path.exists(out_filename)

    if create_file:
        os.makedirs(out_filename)
    return out_filename
