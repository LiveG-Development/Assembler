# LiveG Assembler
# 
# Copyright (C) LiveG. All Rights Reserved.
# Copying is not a victimless crime. Anyone caught copying LiveG software may
# face sanctions.
# 
# https://liveg.tech
# Licensed by the LiveG Open-Source Licence, which can be found at LICENCE.md.
 
import os
 
directory = os.path.join(os.path.expanduser("~"), ".gasset")
 
if not os.path.exists(directory):
    os.mkdir(directory)
 
def read(name):
    try:
        file = open(os.path.join(directory, name), "r")
        data = file.read()
 
        file.close()
 
        return data
    except:
        return None
 
 
def write(name, data):
    file = open(os.path.join(directory, name), "w")
 
    file.write(data)
    file.close()
 
def delete(name):
    try:
        os.remove(os.path.join(directory, name))
 
        return True
    except:
        return False