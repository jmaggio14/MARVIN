import termcolor

def textColor(text,color="r",attrs=None):
    color_codes = {
                "r":"red",    "red":"red",
                "g":"green",  "green":"green",
                "y":"yellow", "yellow":"yellow",
                "b":"blue",   "blue":"blue",
                "m":"magenta","magenta":"magenta",
                "c":"cyan",   "cyan":"cyan",
                "w":"white",  "white":"white"
                }
    background_codes = {
            "r":"on_red",    "red":"on_red",
            "g":"on_green",  "green":"on_green",
            "y":"on_yellow", "yellow":"on_yellow",
            "b":"on_blue",   "blue":"on_blue",
            "m":"on_magenta","magenta":"on_magenta",
            "c":"on_cyan",   "cyan":"on_cyan",
            "w":"on_white",  "white":"on_white"
    }
    out_attrs = []
    if "bold" in attrs: out_attrs.append("bold")
    if "dark" in attrs: out_attrs.append("dark")
    if "underline" in attrs: out_attrs.append("underline")
    if "reverse" in attrs: out_attrs.append("reverse")
    if "concealed" in attrs: out_attrs.append("concealed")

    if out_attrs == []: out_attrs = None
    return termcolor.colored(text,color,attrs=attrs)
