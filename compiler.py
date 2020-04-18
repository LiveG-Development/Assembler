# LiveG Assembler
# 
# Copyright (C) LiveG. All Rights Reserved.
# Copying is not a victimless crime. Anyone caught copying LiveG software may
# face sanctions.
# 
# https://liveg.tech
# Licensed by the LiveG Open-Source Licence, which can be found at LICENCE.md.

import libs.output as output
import libs.lang as lang

import libs.strings.en_GB

_ = lang._

def compile(infile, outfile, size = 6144):
    file = open(infile, "r")
    code = file.read()

    file.close()

    sequence = code.split("\n")
    definitions = {}
    assembled = [0] * size
    position = 0

    print("")

    for i in range(0, len(sequence)) :
        currentLine = sequence[i].strip()
        currentLineSplit = currentLine.split(";")[0].replace("   ", "").replace("  ", "").split(" ")

        output.action(currentLine)

        for j in range(0, len(currentLineSplit)):
            if len(currentLineSplit[j]) > 1 and (currentLineSplit[j][0] == "." or (currentLineSplit[j][0] == "@" and currentLineSplit[j][1] == ".")):
                # Data from definition

                if len(currentLineSplit[j][1]) > 0 and currentLineSplit[j][0] == "@":
                    if currentLineSplit[j][2:] in definitions:
                        currentLineSplit[j] = "@" + definitions[currentLineSplit[j][2:]]
                    else:
                        output.warning("      " + _("definitionDoesNotExist", [i + 1]))
                elif len(currentLineSplit[j][1]) > 0:
                    if currentLineSplit[j][1:] in definitions:
                        currentLineSplit[j] = definitions[currentLineSplit[j][1:]]
                    else:
                        output.warning("      " + _("definitionDoesNotExist", [i + 1]))

        if currentLineSplit[0] == "#define":
            print("      " + _("definition"))

            original = currentLineSplit[1]
            replacement = " ".join(currentLineSplit[2:])

            print("          " + _("definitionOriginal", [original]))
            print("          " + _("definitionReplacement", [original]))

            definitions[original] = replacement
        elif currentLineSplit[0] == "#data":
            print("      " + _("data"))

            startingAddress = int(currentLineSplit[1], 16)

            print("          " + _("dataAddress", [hex(startingAddress)[2:].zfill(2)]))
            
            if currentLineSplit[2][0] == "\"":
                # string

                print("          " + _("dataTypeString"))
                
                allocation = ""
                inString = False
                
                for j in range(0, len(currentLine)):
                    if currentLine[j] == "\"":
                        if inString:
                            break
                        else:
                            inString = True
                    elif inString:
                        allocation += currentLine[j]
                
                allocation = allocation.replace("\\n", "\n")

                for j in range(0, len(allocation)):
                    assembled[startingAddress + j] = ord(allocation[j])
            elif len(currentLineSplit[2]) == 2:
                # byte

                print("          " + _("dataTypeByte"))

                assembled[startingAddress] = int(currentLineSplit[2], 16)
            elif len(currentLineSplit[2]) == 4:
                # int/uint

                print("          "  + _("dataTypeIntUint"))

                assembled[startingAddress] = int(currentLineSplit[2][0:2], 16)
                assembled[startingAddress + 1] = int(currentLineSplit[2][2:4], 16)
            else:
                output.error(_("invalidDataStructure", [i + 1]))

                return
        elif currentLineSplit[0] == "#at":
            position = int(currentLineSplit[1], 16)
        elif currentLine != "" and currentLine[0] != ";":
            print("      " + _("instruction"))

            instructions = {
                "halt": 0x00,
                "allocate": 0x01,
                "copy": 0x02,
                "jump": 0x03,
                "write": 0x04,
                "read": 0x05,
                "add": 0x06,
                "sub": 0x07,
                "mul": 0x08,
                "div": 0x09,
                "mod": 0x0A,
                "equ": 0x0B,
                "neq": 0x0C,
                "ltn": 0x0D,
                "gtn": 0x0E,
                "func": 0x0F,
                "ret": 0x10,
                "sreg": 0x11,
                "sgp": 0x12,
                "cgp": 0x13,
                "dwrite": 0x14,
                "dread": 0x15,
                "bsl": 0x16,
                "bsr": 0x17,
                "and": 0x18,
                "or": 0x19,
                "xor": 0x1A,
                "onec": 0x1B,
                "outbin": 0xA0,
                "outdec": 0xA1,
                "outhex": 0xA2,
                "outasc": 0xA3,
                "in": 0xA4,
                "len": 0xA5,
                "strnum": 0xA6,
                "numstr": 0xA7,
                "dnumstr": 0xA8,
                "fopen": 0xB0,
                "fclose": 0xB1,
                "fwrite": 0xB2,
                "fwriter": 0xB3,
                "fappend": 0xB4,
                "fread": 0xB5,
                "freadr": 0xB6,
                "fsize": 0xB7,
                "fdel": 0xB8,
                "fmd": 0xB9,
                "frd": 0xBA,
                "fstart": 0xBB,
                "fnext": 0xBC,
                "fex": 0xBD,
                "fdir": 0xBE,
                "gpos": 0xC0,
                "gsize": 0xC1,
                "ginit": 0xC2,
                "gfill": 0xC3,
                "gpixel": 0xC4,
                "gline": 0xC5,
                "gfline": 0xC6,
                "grect": 0xC7,
                "gcircle": 0xC8,
                "gbin": 0xC9,
                "gdec": 0xCA,
                "ghex": 0xCB,
                "gasc": 0xCC,
                "gbmp": 0xCD,
                "gtouch": 0xCE,
                "sleep": 0xD0,
                "gyear": 0xD1,
                "gmonth": 0xD2,
                "gdate": 0xD3,
                "gday": 0xD4,
                "ghour": 0xD5,
                "gmin": 0xD6,
                "gsec": 0xD7,
                "sdate": 0xD8,
                "stime": 0xD9
            }

            if currentLineSplit[0] in instructions:
                instruction = instructions[currentLineSplit[0]]
                params = []

                print("          " + _("instructionInstruction", [currentLineSplit[0], hex(instruction)[2:].zfill(2)]))

                for i in range(0, len(currentLineSplit) - 1):
                    params.append(currentLineSplit[i + 1])

                print("          " + _("instructionParameters", [" ".join(str(k) for k in params)]))
                
                for i in range(0, len(params)):
                    if params[i].strip() != "":
                        if params[i][0] == "@":
                            assembled[position] = 0xFF
                            assembled[position + 1] = i

                            if len(params[i]) == 3:
                                assembled[position + 2] = 0
                                assembled[position + 3] = int(params[i][1:], 16)
                            else:
                                assembled[position + 2] = int(params[i][1:3], 16)
                                assembled[position + 3] = int(params[i][3:5], 16)
                        elif params[i][0] == "$":
                            registerConversions = {
                                "PC": 0,
                                "RM": 1,
                                "AR": 2,
                                "ER": 3,
                                "FR": 4,
                                "PM1": 5,
                                "PM2": 6,
                                "PM3": 7,
                                "GX": 8,
                                "GY": 9,
                                "GW": 10,
                                "GH": 11,
                                "GP1": 12,
                                "GP2": 13,
                                "GP3": 14,
                                "GP4": 15,
                                "GP5": 16,
                                "GP6": 17,
                                "GP7": 18,
                                "GP8": 19
                            }

                            assembled[position] = 0xFE
                            assembled[position + 1] = i

                            assembled[position + 2] = 0
                            assembled[position + 3] = registerConversions[params[i][1:]]
                        else:
                            assembled[position] = 0xFD
                            assembled[position + 1] = i
                            
                            if len(params[i].strip()) == 2:
                                assembled[position + 2] = 0
                                assembled[position + 3] = int(params[i].strip(), 16)
                            else:
                                assembled[position + 2] = int(params[i].strip()[0:2], 16)
                                assembled[position + 3] = int(params[i].strip()[2:4], 16)
                        
                        position += 4
            
                assembled[position] = instruction
                position += 1
            else:
                output.error(_("invalidInstruction", [str(i + 1)]))

                return

    while assembled[len(assembled) - 1] == 0:
        assembled.pop()

    file = open(outfile, "wb")
    file.write(bytearray(assembled))
    file.close()

    return [len(assembled), size, (len(assembled) / size) * 100]