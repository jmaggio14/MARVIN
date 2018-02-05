#
# marvin (c) by Jeffrey Maggio, Hunter Mellema, Joseph Bartelmo
#
# marvin is licensed under a
# Creative Commons Attribution-ShareAlike 4.0 International License.
#
# You should have received a copy of the license along with this
# work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.
#
#
"""
License header enforcer for this project
"""
import sys
import os

SKIP = ['.git', 'LICENSE']

LICENSE_HEADER = """
marvin (c) by Jeffrey Maggio, Hunter Mellema, Joseph Bartelmo

marvin is licensed under a
Creative Commons Attribution-ShareAlike 4.0 International License.

You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.

"""

EXTENSIONS_DICT = {'py': '#',\
        'js': '//',\
        'sh': '#',\
        'gitignore': '#',\
        'Dockerfile': '#',\
        'yml': '#',\
        'rc': '#',\
        'java': '//',\
        'c': '//',\
        'cpp': '//',\
        'h': '//',\
        'hpp': '//',\
        'rb': '#',\
        }

def generate_header(unformatted_license, filename):
    """
    Generates the list of strings specific to the given character as
    a comment
    :returns license header lines in list
    """
    extension = filename.split('/')[-1].split('\\')[-1].split('.')[-1]
    if extension not in EXTENSIONS_DICT:
        print('Warning: unknown extension associated with:', filename)
        return []
    char = EXTENSIONS_DICT[extension]
    return [(char + ' ' + line).rstrip()\
            for line in unformatted_license.split('\n')]

def check_valid_header(header, filename):
    """
    Checks to see if the given file contents has a valid header on top
    """
    with open(filename, 'r') as filestream:
        content = filestream.read().split('\n')
        if len(content) < len(header):
            return False
        for (headerline, contentline) in zip(header, content):
            if headerline != contentline:
                return False
    return True

def print_valid_header(header, filename):
    """
    Simply checks to see if the header is valid, and prints accordingly
    """
    if check_valid_header(header, filename):
        print('Valid:', filename)
        return 0
    print('Invalid', filename)
    return -1

def apply_header(header, filename):
    """
    Applies the generated license header to the target file, comment
    for license header is generated through the extension dictionary

    :return True on success, false if unknown extension
    """
    if print_valid_header(header, filename) == 0:
        return 0
    with open(filename, 'r+') as filestream:
        content = filestream.read()
        filestream.seek(0)
        filestream.write("\n".join(header) + "\n")
        filestream.write(content)
    return 0

def evaluate_header(header, filename, modify):
    """
    Runs either the apply_header or print_valid_header
    depending on modify boolean
    """
    try:
        if modify:
            return apply_header(header, filename)
        return print_valid_header(header, filename)
    except UnicodeDecodeError:
        return 0

def enforce_header(unformatted_license, directory, modify=False):
    """
    Recursively iterates over target directory and finds all known
    file types and checks to see whether or not they conform to the header
    :arg modify If modify is set to True then it will inject the header if it
    does not exist
    :return 0 on success, -1 on failure
    """
    returns = 0
    if os.path.isfile(os.path.abspath(directory)):
        header = generate_header(unformatted_license, directory)
        return evaluate_header(header, directory, modify)
    for obj in os.listdir(directory):
        if obj not in SKIP:
            if os.path.isfile(os.path.abspath(obj)):
                header = generate_header(unformatted_license, obj)
                if evaluate_header(header, obj, modify) == -1:
                    returns = -1
            elif enforce_header(unformatted_license,\
                    os.path.join(directory, obj)) == -1:
                returns = -1
    return returns

if __name__ == '__main__':
    RESULT = enforce_header(LICENSE_HEADER, './', False)
    if RESULT == 0:
        print('Successful enforcement')
    else:
        print('Failed enforcement')
    sys.exit(RESULT)
