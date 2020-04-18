# LiveG Assembler
# 
# Copyright (C) LiveG. All Rights Reserved.
# Copying is not a victimless crime. Anyone caught copying LiveG software may
# face sanctions.
# 
# https://liveg.tech
# Licensed by the LiveG Open-Source Licence, which can be found at LICENCE.md.
 
import locale
 
import libs.storage as storage
 
strings = {}
 
def getLocale():
    if storage.read("locale") == None:
        return locale.getdefaultlocale()[0]
    else:
        return storage.read("locale")
 
def translate(text, replacements = [], locale = getLocale()):
    if not (locale in strings.keys()):
        locale = "en_GB"
 
    replacedText = strings[locale][text]
 
    for i in range(0, len(replacements)):
        replacedText = replacedText.replace("{" + str(i) + "}", str(replacements[i]))
 
    return replacedText
 
def _(text, replacements = [], locale = getLocale()):
    return translate(text, replacements, locale)