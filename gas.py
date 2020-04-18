# LiveG Assembler
# 
# Copyright (C) LiveG. All Rights Reserved.
# Copying is not a victimless crime. Anyone caught copying LiveG software may
# face sanctions.
# 
# https://liveg.tech
# Licensed by the LiveG Open-Source Licence, which can be found at LICENCE.md.

import os
import sys
import shutil
import subprocess
import contextlib

import libs.colours as colours
import libs.storage as storage
import libs.output as output
import libs.lang as lang
import compiler

import libs.strings.en_GB

_ = lang._

VERSION = "V0.1.0"

args = sys.argv

requiredInstalls = False

if (len(args) > 1 and (args[1] == "--hide" or args[1] == "-h")):
    args.pop(1)
elif storage.read("hide") != "true":
    print(_("welcome", [colours.get("lred"), colours.get("white"), VERSION]))
    print(_("copyright"))
    print("")

    if storage.read("locale") == None:
        output.warning(_("setLocaleWarning", [lang.getLocale()]))
        print("")

# Install libraries for when they don't exist
def installLib(name, description):
    global requiredInstalls

    requiredInstalls = True

    output.action(_("installRequiredLibs", [description]))

    returns = subprocess.call([sys.executable, "-m", "pip", "install", name], stdout = subprocess.PIPE, stderr = subprocess.PIPE)

    if returns != 0:
        output.error(_("installRequiredLibsError"))

        sys.exit(1)

# Try importing the libraries, if not install them
try:
    with contextlib.redirect_stdout(None):
        import pygame
except:
    installLib("pygame", "installGraphicsLibrary")

if requiredInstalls: print("")

# Finally, import any local code that require the external libraries
import runtime

def stringIsInt(string):
    try: 
        int(string)

        return True
    except ValueError:
        return False

def useIntOrDefault(string, default):
    if string != None and stringIsInt(string):
        return int(string)
    else:
        return default

# CLI section
if len(args) == 1:
    print(_("help"))
else:
    if args[1] == "help" or args[1] == "--help" or args[1] == "/?":
        print(_("help"))
    elif args[1] == "var":
        try:
            if len(args) > 2:
                name = args[2]

                if len(args) == 3:
                    if storage.read(name) == None:
                        output.error(_("varNoMatch", [name]))
                        sys.exit(1)
                    else:
                        output.returns(_("varReturn", [name, storage.read(name)]))
                elif len(args) == 4:
                    if args[3] == "--delete":
                        if storage.delete(name):
                            output.returns(_("varDeleteSuccess", [name]))
                        else:
                            output.error(_("varDeleteFail", [name]))
                            sys.exit(1)
                    else:
                        data = args[3]

                        storage.write(name, data)

                        output.returns(_("varWriteReturn", [name, data]))
                else:
                    output.error(_("invalidCommandStructure"))
                    sys.exit(1)
            else:
                output.error(_("invalidCommandStructure"))
                sys.exit(1)
        except:
            output.error(_("varError"))
            sys.exit(1)
    elif args[1] == "compile":
        if len(args) > 2:
            infile = args[2]
            outfile = ""
            size = useIntOrDefault(storage.read("size"), 6144)

            if len(args) > 3:
                outfile = args[3]
            else:
                outfile = "".join(infile.split("/")[-1].split(".")[:-1]) + ".gbn"

            output.returns(_("programUsage", compiler.compile(infile, outfile, size)))
        else:
            output.error(_("invalidCommandStructure"))
            sys.exit(1)
    elif args[1] == "build":
        size = useIntOrDefault(storage.read("size"), 6144)
        filesCompiled = 0
        librariesCompiled = 0

        output.action(_("cleanUpBuildDir"))

        try:
            shutil.rmtree("build")
        except:
            pass
    
        definitions = {}

        for compilePass in range(0, 2):
            if compilePass == 0:
                output.action(_("buildLibraries"))
            else:
                output.action(_("buildFiles"))

            for root, subdirs, files in os.walk(".", topdown = True):
                neededPath = os.path.join("build", root)

                # Skip the `build` directory
                if root.startswith(os.path.join(".", "build", "")):
                    continue

                # Skip the `.git` directory so that git objects don't get copied
                if root.startswith(os.path.join(".", ".git", "")):
                    continue
                    
                if not os.path.exists(neededPath):
                    os.makedirs(neededPath)
                
                for i in range(0, len(files)):
                    infile = os.path.join(root, files[i])
                    outfile = os.path.join(neededPath, files[i])

                    if files[i].endswith(".gas") and compilePass != 0:
                        output.action(_("compileFile", [os.path.join(root, files[i])]))

                        definitions = compiler.compile(infile, ".".join(outfile.split(".")[:-1]) + ".gbn", size, definitions)["definitions"]

                        filesCompiled += 1
                    elif files[i].endswith(".gal") and compilePass != 1:
                        output.action(_("compileLibrary", [os.path.join(root, files[i])]))

                        definitions = compiler.compile(infile, ".".join(outfile.split(".")[:-1]) + ".gbl", size, definitions)["definitions"]
                        filesCompiled += 1
                        librariesCompiled += 1
                    elif compilePass != 0:
                        output.action(_("copyFile", [os.path.join(root, files[i])]))

                        infileOpen = open(infile, "rb")
                        infileData = infileOpen.read()
                        outfileOpen = open(outfile, "wb")

                        outfileOpen.write(infileData)

                        infileOpen.close()
                        outfileOpen.close()
            
        output.returns(_("compiledFiles", [filesCompiled, librariesCompiled]))
    elif args[1] == "run":
        if len(args) > 2:
            filename = args[2]
            size = useIntOrDefault(storage.read("size"), 6144)
            built = False
            debugging = False

            if len(args) > 3:
                if args[3] == "--built":
                    built = True
                if args[3] == "--debug":
                    debugging = True

                if len(args) > 4:
                    if args[4] == "--built":
                        built = True
                    if args[4] == "--debug":
                        debugging = True
            
            if built: os.chdir("build")
            
            runtime.run(filename, size, debugging)

            if built: os.chdir("..")
        else:
            output.error(_("invalidCommandStructure"))
            sys.exit(1)
    else:
        output.error(_("invalidCommand"))
        sys.exit(1)

sys.exit(0)