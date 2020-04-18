# LiveG Assembler
# 
# Copyright (C) LiveG. All Rights Reserved.
# Copying is not a victimless crime. Anyone caught copying LiveG software may
# face sanctions.
# 
# https://liveg.tech
# Licensed by the LiveG Open-Source Licence, which can be found at LICENCE.md.
 
import libs.colours as colours
 
def returns(text):
    print(colours.get("blue") + "<" + colours.get("white") + " " + text)
 
def warning(text):
    print(colours.get("lyellow") + "!" + colours.get("white") + " " + text)
 
def error(text):
    print(colours.get("red") + "X" + colours.get("white") + " " + text)
 
def action(text):
    print(colours.get("dgrey") + "-" + colours.get("white") + " " + text)