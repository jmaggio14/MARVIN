import os
import marvin

def preventOverwrite(filename,create_file=True):
    """
    checks to see if a file or directory already exists and creates a new filename
    if it does. It can also create the file if specificed

    when creating a file, this function assumes that if there is no file extension
    then it should create a directory

    NOTE:
        this function is referenced (as of Nov, 2017) in marvin's init() function
        and therefore cannot be modifed to require post-initialization global variables

    input::
        filename (str): the full file or directory path to be overwrite protected
        create_file (bool): boolean indicating whether or not to create the file
                        before returning
    return::
        out_filename (str): the assuredly unique output filename
    """
    basefilename,extension = os.path.splitext(filename)
    out_filename = filename
    file_exists = os.path.exists(out_filename)
    num = 1

    if extension == "":
        input_is_directory = True
    else:
        input_is_directory = False

    while file_exists:
        if input_is_directory:
            out_filename = basefilename[:-1] + marvin.fileNumber(num,0) + "/"
        else:
            out_filename =  basefilename + marvin.fileNumber(num,0) + extension
        num += 1
        file_exists = os.path.exists(out_filename)

    if create_file:
        if extension == "":
            os.makedirs(out_filename)
        else:
            base_path = os.path.split(out_filename)[0]
            if not os.path.exists(base_path):
                os.makedirs(base_path)
            with open(out_filename,"w") as out:
                out.write("")

    return out_filename


def fileNumber(file_number,number_digits=5):
    """
    returns a number string designed to be used in the prefix of systematic outputs.
    example use case
        "00001example_output_file.txt"
        "00002example_output_file.txt"

    input::
        file_number (str,int): number of file
        number_digits (int): number of digits in the output string
    return::
        numbered_string (str): string of numbers with standard number of digits
    """
    file_number_string = str(file_number)
    len_num_string = len(file_number_string)

    if len_num_string < number_digits:
        prefix = "0" * (number_digits - len_num_string)
    else:
        prefix = ""

    numbered_string = prefix + file_number_string
    return numbered_string
