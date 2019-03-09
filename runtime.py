# LiveG Assembler
# 
# Copyright (C) LiveG. All Rights Reserved.
# Copying is not a victimless crime. Anyone caught copying LiveG software may
# face sanctions.
# 
# https://liveg.tech
# Licensed by the LiveG Open-Source Licence, which can be found at LICENCE.md.

import os
import contextlib

try:
    with contextlib.redirect_stdout(None):
        import pygame
except ImportError:
    raise ImportError("please install PyGame to use LiveG Assembler")

try:
    import drawtools
except ImportError:
    raise ImportError("drawtools.py is missing, it is needed for graphics")

registers = [0] * 20
memory = [0] * 6144

fileDirectory = ""

filename = input("File? ")
debugging = input("Debug (y)? ") == "y"
file = open(filename, "rb")
position = 0

while True:
    c = file.read(1)

    if not c:
        break
    
    memory[position] = ord(c)
    position += 1

file.close()

if debugging: print("Memory dump:\n" + " ".join(hex(i)[2:].zfill(2) for i in memory))

running = True

while running:
    instruction = memory[registers[0]]
    parameters = []

    for i in range(5, 8):
        parameters.append(registers[i])

    if debugging:
        print("Instruction: " + hex(instruction)[2:].zfill(2))
        print("Parameters: " + hex(parameters[0])[2:].zfill(2) + ", " + hex(parameters[1])[2:].zfill(2) + ", " + hex(parameters[2])[2:].zfill(2))

    if instruction == 0x00:
        # halt

        running = False
    elif instruction == 0x01:
        # allocate

        for i in range(0, parameters[1]):
            memory[parameters[0] + i] = 0
    elif instruction == 0x02:
        # copy

        for i in range(0, parameters[1]):
            memory[parameters[2] + i] = memory[parameters[0] + i]
    elif instruction == 0x03:
        # jump

        registers[0] = parameters[0]
    elif instruction == 0x04:
        # write

        affectedValue = parameters[0]

        while affectedValue >= 256:
            affectedValue = affectedValue - 256
        
        memory[parameters[1]] = affectedValue
    elif instruction == 0x05:
        # read

        registers[1] = memory[parameters[0]]
    elif instruction == 0x06:
        # add

        registers[2] = parameters[0] + parameters[1]

        registers[3] = 0
    elif instruction == 0x07:
        # sub

        registers[2] = parameters[0] - parameters[1]

        if registers[2] < 0:
            registers[2] = 65536 + registers[2]

        registers[3] = 0
    elif instruction == 0x08:
        # mul

        registers[2] = parameters[0] * parameters[1]

        registers[3] = 0
    elif instruction == 0x09:
        # div

        if parameters[1] == 0:
            registers[3] = 1
        else:
            registers[2] = parameters[0] // parameters[1]

            registers[3] = 0
    elif instruction == 0x0A:
        # mod

        if parameters[1] == 0:
            registers[3] = 1
        else:
            registers[2] = parameters[0] % parameters[1]

            registers[3] = 0
    elif instruction == 0x0B:
        # equ

        if parameters[0] == parameters[1]:
            registers[0] = parameters[2]
        else:
            registers[0] += 1
    elif instruction == 0x0C:
        # neq

        if parameters[0] != parameters[1]:
            registers[0] = parameters[2]
        else:
            registers[0] += 1
    elif instruction == 0x0D:
        # ltn

        if parameters[0] < parameters[1]:
            registers[0] = parameters[2]
        else:
            registers[0] += 1
    elif instruction == 0x0E:
        # gtn

        if parameters[0] > parameters[1]:
            registers[0] = parameters[2]
        else:
            registers[0] += 1
    elif instruction == 0x0F:
        # func
        
        registers[4] = registers[0]
        registers[0] = parameters[0]
    elif instruction == 0x10:
        # ret

        registers[0] = registers[4]
        registers[4] = 0
    elif instruction == 0x11:
        # sreg

        registers[parameters[0]] = parameters[1]
    elif instruction == 0x12:
        # sgp

        registers[parameters[0] + 11] = parameters[1]
    elif instruction == 0x13:
        # cgp

        for i in range(12, 20):
            registers[i] = 0
    elif instruction == 0x14:
        # dwrite

        byteA = (parameters[0] >> 8) & 0xFF
        byteB = parameters[0] & 0xFF

        memory[parameters[1]] = byteA
        memory[parameters[1] + 1] = byteB
    elif instruction == 0x15:
        # dread

        registers[1] = (memory[parameters[0]] * 256) + memory[parameters[0] + 1]
    elif instruction == 0xA0:
        # outbin

        for i in range(0, parameters[1]):
            print("{0:b}".format(memory[parameters[0] + i]), end = "", flush = True)
    elif instruction == 0xA1:
        # outdec

        result = 0

        for i in range(0, parameters[1]):
            result = (result * 256) + memory[parameters[0] + i]

        print(result, end = "", flush = True)
    elif instruction == 0xA2:
        # outhex

        for i in range(0, parameters[1]):
            if len(hex(memory[parameters[0] + i])[2:]) < 1:
                print(hex(memory[parameters[0] + i])[2:], end = "", flush = True)
            else:
                print("0" + hex(memory[parameters[0] + i])[2:], end = "", flush = True)
    elif instruction == 0xA3:
        # outasc

        for i in range(0, parameters[1]):
            print(chr(memory[parameters[0] + i]), end = "", flush = True)
    elif instruction == 0xA4:
        # in

        entered = input("")

        for i in range(0, parameters[1]):
            if i < len(entered):
                memory[parameters[0] + i] = ord(entered[i])
    elif instruction == 0xA5:
        # len

        currentChar = 0

        while memory[parameters[0] + currentChar] != parameters[1]:
            currentChar += 1
        
        registers[1] = currentChar
    elif instruction == 0xA6:
        # strnum

        number = 0
        error = False

        for i in range(0, parameters[1]):
            if chr(memory[parameters[0] + i]) in "0123456789":
                number = (number * 10) + int(chr(memory[parameters[0] + i]))
            else:
                error = True
        
        registers[1] = number

        registers[3] = error * 2
    elif instruction == 0xB0:
        # fopen

        fileDirectory = ""

        for i in range(0, parameters[1]):
            fileDirectory += chr(memory[parameters[0] + i])
        
        registers[3] = 0
    elif instruction == 0xB1:
        # fclose

        fileDirectory = ""
    elif instruction == 0xB2:
        # fwrite

        if fileDirectory != "":
            try:
                os.remove(fileDirectory)
            except:
                pass

            file = open(fileDirectory, "w")

            for i in range(0, parameters[1]):
                file.write(chr(memory[parameters[0] + i]))

            file.close()

            registers[3] = 3
        else:
            registers[3] = 0
    elif instruction == 0xB3:
        # fwriter

        if fileDirectory != "":
            file = open(fileDirectory, "r+")

            file.seek(parameters[2])

            for i in range(0, parameters[1]):
                file.write(chr(memory[parameters[0] + i]))

            file.close()

            registers[3] = 3
        else:
            registers[3] = 0
    elif instruction == 0xB4:
        # fappend

        if fileDirectory != "":
            file = open(fileDirectory, "a")

            for i in range(0, parameters[1]):
                file.write(chr(memory[parameters[0] + i]))

            file.close()

            registers[3] = 3
        else:
            registers[3] = 0
    elif instruction == 0xB5:
        # fread

        if fileDirectory != "":
            file = open(fileDirectory, "r")

            if parameters[0] + parameters[1] <= 6144:
                for i in range(0, parameters[1]):
                    nextChar = file.read(1)

                    if nextChar:
                        memory[parameters[0] + i] = ord(nextChar)
                    else:
                        registers[3] = 4
            else:
                registers[3] = 5

            file.close()

            registers[3] = 3
        else:
            registers[3] = 0
    elif instruction == 0xB6:
        # freadr

        if fileDirectory != "":
            file = open(fileDirectory, "r")

            file.seek(parameters[2])

            if parameters[0] + parameters[1] <= 6144:
                for i in range(0, parameters[1]):
                    nextChar = file.read(1)

                    if nextChar:
                        memory[parameters[0] + i] = ord(nextChar)
                    else:
                        parameters[3] = 4
            else:
                registers[3] = 5

            file.close()

            registers[3] = 3
        else:
            registers[3] = 0
    elif instruction == 0xB7:
        # fsize

        if fileDirectory != "":
            registers[1] = os.path.getsize(os.path.join(os.getcwd(), fileDirectory))

            registers[3] = 0
        else:
            registers[3] = 3
    elif instruction == 0xFD:
        # (setpar)
        # Uses raw parameters only. Registers can't be used!

        registers[memory[registers[0] + 1] + 5] = (memory[registers[0] + 2] * 256) + memory[registers[0] + 3]
    elif instruction == 0xFE:
        # (regpar)
        # Uses raw parameters only. Registers can't be used!
       
        registers[memory[registers[0] + 1] + 5] = registers[memory[registers[0] + 3]]
    elif instruction == 0xFF:
        # (loadpar)
        # Uses raw parameters only. Registers can't be used!
        registers[memory[registers[0] + 1] + 5] = memory[(memory[registers[0] + 2] * 256) + memory[registers[0] + 3]]
    
    if instruction != 0x03 and instruction != 0x0B and instruction != 0x0C and instruction != 0x0D and instruction != 0x0E and instruction != 0x0F and instruction != 0x10:
        # Only increase PC if jump instruction isn't used

        if instruction == 0xFD or instruction == 0xFE or instruction == 0xFF:
            # Jump by 4 in parameter instructions

            registers[0] += 4
        else:
            # Just jump by 1
            registers[0] += 1

if debugging: print("Halted, memory dump:\n" + " ".join(hex(i)[2:].zfill(2) for i in memory))