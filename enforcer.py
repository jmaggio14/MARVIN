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

EXTENSIONS_DICT = { 'py': '#',\
        'js': '\\\\',\
        'sh': '#',\
        'gitignore': '#',\
        'md': '#',\
        'Dockerfile': '#',\
        'yml': '#',\
        'rc': '#',\
        }

def generate_header(char):
    license = []
    split_license = LICENSE_HEADER.split('\n')
    for line in split_license:
        license.append((char + ' ' + line).rstrip())
    return license, len(split_license)

def apply_header(filename):
    extension = filename.split('/')[-1].split('\\')[-1].split('.')[-1]
    if extension not in EXTENSIONS_DICT:
        print 'Warning: unknown extension associated with:', filename
        return False
    license, lines = generate_header(EXTENSIONS_DICT[extension])
    with open(filename, 'r+') as filestream:
        content = filestream.read()
        split_content = content.split('\n')
        filestream.seek(0)
        if len(split_content) < lines:
            filestream.write("\n".join(license))
            filestream.write(content)
        else:
            for line in range(0, lines):
                if license[line] != split_content[line]:
                    filestream.write("\n".join(license) + "\n")
                    filestream.write(content)
                    break
        return True

def enforce_header(directory):
    returns = 0
    if os.path.isfile(os.path.abspath(directory)):
        result = apply_header(directory)
        if result:
            print 'Valid:', directory
            return 0
        return -1
    for obj in os.listdir(directory):
        if obj not in SKIP:
            if os.path.isfile(os.path.abspath(obj)):
                if not apply_header(os.path.join(directory, obj)):
                    returns = -1
                else:
                    print 'Valid:', os.path.join(directory, obj)
            elif enforce_header(os.path.join(directory, obj)) == -1:
                returns = -1
            else:
                print 'Valid:', os.path.join(directory, obj)
    return returns

if __name__ == '__main__':
    sys.exit(enforce_header('./'))

