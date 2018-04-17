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
import termcolor

def color_text(text,color="r",background=None,attrs=None):
    """
    adds ansi escape codes to a string to change the color in a terminal
    printout

    using print(color_text_output) with with windows powershell or
    cmd prompt will not yield a colored string

    example::
        >>> warning_msg = color_text('this is a warning',
        ...                                color = 'red',
        ...                                background = 'yellow',
        ...                                attrs = ['bold','underline'])
        >>> warning_msg
        '\x1b[4m\x1b[1m\x1b[43m\x1b[31mthis is a warning\x1b[0m'


    input::
        text (str):
            Input text to colorize
        color (str) = 'r':
                String which indicates the color to use for the text
                acceptable values are:
                                "r",    "red",
                                "g",  "green",
                                "y", "yellow",
                                "b",   "blue",
                                "m", magenta",
                                "c",   "cyan",
                                "w",  "white",
        background (str) = None:
                String which indicates what color to use for the text's
                background colors.
                acceptable values are:
                                "r",    "red",
                                "g",  "green",
                                "y", "yellow",
                                "b",   "blue",
                                "m", magenta",
                                "c",   "cyan",
                                "w",  "white",
        attrs (list,str) = None:
                additional styles that can be applied to the text. This
                can be in the form of a long string or list
                acceptable values are:
                                "bold",
                                "dark",
                                "underline",
                                "reverse",
                                "concealed"

    return::
        colored_text (str):
                string with proper color codes added (colored string)

    """
    assert isinstance(text,str),"'test' must be a string"
    assert isinstance(color,str),"color' must be a string"
    assert isinstance(color,str),"background' must be a string"
    assert isinstance(attrs,(type(None),list,tuple)),\
                                    "'attrs must be a list,tuple,NoneType'"

    color_codes = {
                "r":"red",    "red":"red",
                "g":"green",  "green":"green",
                "y":"yellow", "yellow":"yellow",
                "b":"blue",   "blue":"blue",
                "m":"magenta","magenta":"magenta",
                "c":"cyan",   "cyan":"cyan",
                "w":"white",  "white":"white",
                None:None
                }
    background_codes = {
                "r":"on_red",    "red":"on_red",
                "g":"on_green",  "green":"on_green",
                "y":"on_yellow", "yellow":"on_yellow",
                "b":"on_blue",   "blue":"on_blue",
                "m":"on_magenta","magenta":"on_magenta",
                "c":"on_cyan",   "cyan":"on_cyan",
                "w":"on_white",  "white":"on_white",
                None:None
                }
    if attrs == None:
        attrs = []

    out_attrs = []
    if "bold" in attrs:
        out_attrs.append("bold")
    if "dark" in attrs:
        out_attrs.append("dark")
    if "underline" in attrs:
        out_attrs.append("underline")
    if "reverse" in attrs:
        out_attrs.append("reverse")
    if "concealed" in attrs:
        out_attrs.append("concealed")
    if out_attrs == []:
        out_attrs = None

    #
    if color in color_codes.keys() and background in background_codes.keys():
        text_color = color_codes[color]
        text_background = background_codes[background]

    else:
        error_msg = "invalid color or background code must be one of {all} \
                                        \ncolor input: {color_input} \
                                        \nbackground input: {background_input}"
                                        .format(all=list(color_codes.keys()),
                                                color_input=color,
                                                background_input=background)
        raise ValueError(error_msg)


    kwargs = {"text":text,
                "color":text_color,
                "on_color":text_background,
                "attrs":out_attrs}
    colored_text = termcolor.colored(**kwargs)
    return colored_text



def color_print(msg):
    """direct wrapper for termcolor.cprint

    **may not yield a colored output on windows powershell or cmd line

    input::
        msg(string):
            the string you want to print

    returns::
        None
    """
    termcolor.cprint(msg)






#END
