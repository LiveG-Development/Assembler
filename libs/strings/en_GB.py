# LiveG Assembler
# 
# Copyright (C) LiveG. All Rights Reserved.
# Copying is not a victimless crime. Anyone caught copying LiveG software may
# face sanctions.
# 
# https://liveg.tech
# Licensed by the LiveG Open-Source Licence, which can be found at LICENCE.md.
 
import libs.lang as lang
 
lang.strings["en_GB"] = {
    "welcome": "{0}LiveG Assembler{1} {2}",
    "copyright": "Copyright (C) LiveG. All Rights Reserved.",
    "installRequiredLibs": "Installing required libraries for LiveG Assembler ({0})...",
    "installRequiredLibsError": "Couldn't install required libraries. Try running LiveG Assembler by itself with administrator/superuser privileges.",
    "installGraphicsLibrary": "Graphics library",
    "help": """usage: gas [--hide | -h] <command> [<args>]
 
List of commands used in LiveG Assembler:
    help        Display this help screen.
    var         Read, set or delete variables.
                <name>              Read data contained in variable.
                <name> <data>       Write data to variable.
                <name> --delete     Delete variable.
    compile     Compile a single file into a .gbn file.
                <infile>            Compile <infile> into a .gbn file with the same name (without original file extension).
                <infile> <outfile>  Compile <infile> into <outfile>.
    build       Compile the current directory into the `build` subdirectory.
    run         Run the specified file in an emulator.
                <file>              Run compiled file.
                <file> --built      Run compiled file from within the `build` subdirectory.
                <file> --debug      Run compiled file in debug mode.
                <file> --built --debug
                                    Run compiled file from within the `build` subdirectory in debug mode.
    """,
    "invalidCommand": "Command is invalid.",
    "invalidCommandStructure": "Command structure is invalid.",
    "setLocaleWarning": "Don't forget to set your locale! We've determined locale to be {0}, but to be sure that this is your locale, type:\n    gas var locale {0}",
    "varNoMatch": "No matches found for {0}.",
    "varReturn": "{0}: {1}",
    "varDeleteSuccess": "Deleted {0}.",
    "varDeleteFail": "Could not delete {0}. {0} may not exist or may have special permissions.",
    "varWriteReturn": "Set {0} to {1}.\n{0}: {1}",
    "varError": "Could not perform action. Check that the variable in use isn't reserved.",
    "definition": "definition",
    "definitionOriginal": "original: {0}",
    "definitionReplacement": "replacement: {0}",
    "definitionDoesNotExist": "Definition does not exist on line {0}, continuing",
    "data": "data",
    "dataAddress": "address: {0}",
    "dataTypeString": "type: string",
    "dataTypeByte": "type: byte",
    "dataTypeIntUint": "type: int/uint",
    "invalidDataStructure": "Invalid data structure on line {0}",
    "instruction": "instruction",
    "instructionInstruction": "instruction: {0} ({1})",
    "instructionParameters": "parameters: {0}",
    "instructionHex": "instruction: {0}",
    "invalidInstruction": "Invalid instruction on line {0}.",
    "programUsage": "Compiled; program uses {0}/{1} bytes, {2}% of memory.",
    "cleanUpBuildDir": "Cleaning up `build` directory...",
    "compileFile": "Compiling {0}...",
    "compileLibrary": "Compiling library {0}...",
    "copyFile": "Copying {0}...",
    "compiledFiles": "Successfully compiled! Files: {0}, of which libraries: {1}",
    "startMemoryDump": "Start memory dump:\n{0}",
    "halted": "Halted.",
    "haltedEndMemoryDump": "Halted, end memory dump:\n{0}"
}