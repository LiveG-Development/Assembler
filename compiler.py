# LiveG Assembler
# 
# Copyright (C) LiveG. All Rights Reserved.
# Copying is not a victimless crime. Anyone caught copying LiveG software may
# face sanctions.
# 
# https://liveg.tech
# Licensed by the LiveG Open-Source Licence, which can be found at LICENCE.md.

infile = input("File in? ")
outfile = input("File out? ")
file = open(infile, "r")
code = file.read()
file.close()

sequence = code.split("\n")
assembled = [0] * 6144
position = 0

print("")

for i in range(0, len(sequence)) :
    currentLine = sequence[i].strip()
    currentLineSplit = currentLine.split(";")[0].replace("  ", "").split(" ")

    print(currentLine)

    if currentLineSplit[0] == "#data":
        print("    data")

        startingAddress = int(currentLineSplit[1], 16)

        print("        address: " + hex(startingAddress)[2:].zfill(2))

        if currentLineSplit[2][0] == "\"":
            # string

            print("        type: string")
            
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

            print("        type: byte")

            assembled[startingAddress] = int(currentLineSplit[2], 16)
        elif len(currentLineSplit[2]) == 4:
            # int/uint

            print("        type: int/uint")

            assembled[startingAddress] = int(currentLineSplit[2][0:2], 16)
            assembled[startingAddress + 1] = int(currentLineSplit[2][2:4], 16)
        else:
            raise TypeError("invalid data structure on line " + str(i + 1))
    elif currentLineSplit[0] == "#at":
        position = int(currentLineSplit[1], 16)
    elif currentLine != "" and currentLine[0] != ";":
        print("    instruction")

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
            "dwrite": 0x14,
            "dread": 0x15,
            "outbin": 0xA0,
            "outdec": 0xA1,
            "outhex": 0xA2,
            "outasc": 0xA3
        }

        if currentLineSplit[0] in instructions:
            instruction = instructions[currentLineSplit[0]]
            params = []

            print("        instruction: " + currentLineSplit[0] + " (" + hex(instruction)[2:].zfill(2) + ")")

            for i in range(0, len(currentLineSplit) - 1):
                params.append(currentLineSplit[i + 1])

            print("        params: " + (" ".join(str(k) for k in params)))
            
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
                            "PM3": 7
                        }

                        assembled[position] = 0xFE
                        assembled[position + 1] = i

                        assembled[position + 2] = 0
                        assembled[position + 3] = registerConversions[params[i][1:]]
                    else:
                        assembled[position] = 0xFD
                        assembled[position + 1] = i
                        
                        if len(params[i]) == 2:
                            assembled[position + 2] = 0
                            assembled[position + 3] = int(params[i], 16)
                        else:
                            assembled[position + 2] = int(params[i][0:2], 16)
                            assembled[position + 3] = int(params[i][2:4], 16)
                    
                    position += 4
        
            assembled[position] = instruction
            position += 1
        else:
            raise NameError("invalid instruction on line " + str(i + 1) + ".")

while assembled[len(assembled) - 1] == 0:
    assembled.pop()

print("")

print("Code dump:\n" + " ".join(hex(i)[2:].zfill(2) for i in assembled))
print("Program uses " + str(len(assembled)) + "/6144 bytes, " + str((len(assembled) / 6144) * 100) + "% of memory")

file = open(outfile, "wb")
file.write(bytearray(assembled))
file.close()