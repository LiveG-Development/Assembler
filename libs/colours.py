# LiveG Assembler
# 
# Copyright (C) LiveG. All Rights Reserved.
# Copying is not a victimless crime. Anyone caught copying LiveG software may
# face sanctions.
# 
# https://liveg.tech
# Licensed by the LiveG Open-Source Licence, which can be found at LICENCE.md.
 
colours = {
    "background": {
        "black": "\033[40m",
        "white": "\033[107m",
        "red": "\033[41m",
        "green": "\033[42m",
        "yellow": "\033[43m",
        "blue": "\033[44m",
        "magenta": "\033[45m",
        "cyan": "\033[46m",
        "lgrey": "\033[47m",
        "dgrey": "\033[100m",
        "lred": "\033[101m",
        "lgreen": "\033[102m",
        "lyellow": "\033[103m",
        "lblue": "\033[104m",
        "lmagenta": "\033[105m",
        "lcyan": "\033[106m"
    },
 
    "foreground": {
        "black": "\033[30m",
        "white": "\033[97m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "lgrey": "\033[37m",
        "dgrey": "\033[90m",
        "lred": "\033[91m",
        "lgreen": "\033[92m",
        "lyellow": "\033[93m",
        "lblue": "\033[94m",
        "lmagenta": "\033[95m",
        "lcyan": "\033[96m"
    }
}
 
def get(colour, background = False):
    if background:
        return colours["background"][colour]
    else:
        return colours["foreground"][colour]