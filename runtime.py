# LiveG Assembler
# 
# Copyright (C) LiveG. All Rights Reserved.
# Copying is not a victimless crime. Anyone caught copying LiveG software may
# face sanctions.
# 
# https://liveg.tech
# Licensed by the LiveG Open-Source Licence, which can be found at LICENCE.md.

from pathlib import Path
import os
import shutil
import time
import datetime

import libs.output as output
import libs.lang as lang
import drawtools

import libs.strings.en_GB

_ = lang._

def run(filename, size = 6144, debugging = False):
    registers = [0] * 20
    memory = [0] * size

    fileDirectory = ""

    file = open(filename, "rb")
    directoryPath = "/"
    directoryPosition = 0
    position = 0

    while True:
        c = file.read(1)

        if not c:
            break
        
        memory[position] = ord(c)
        position += 1

    file.close()

    if debugging: output.action(_("startMemoryDump", [" ".join(hex(i)[2:].zfill(2) for i in memory)]))

    running = True

    while running:
        instruction = memory[registers[0]]
        parameters = []

        for i in range(5, 8):
            parameters.append(registers[i])

        if debugging:
            output.action(_("instructionHex", [hex(instruction)[2:].zfill(2)]))
            print("      " + _("instructionParameters", [hex(parameters[0])[2:].zfill(2) + ", " + hex(parameters[1])[2:].zfill(2) + ", " + hex(parameters[2])[2:].zfill(2)]))

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
        elif instruction == 0x16:
            # bsl

            registers[2] = (parameters[0] << parameters[1]) & 0xFFFF
        elif instruction == 0x17:
            # bsr

            registers[2] = (parameters[0] >> parameters[1]) & 0xFFFF
        elif instruction == 0x18:
            # and

            registers[2] = parameters[0] & parameters[1]
        elif instruction == 0x19:
            # or

            registers[2] = parameters[0] | parameters[1]
        elif instruction == 0x1A:
            # xor

            registers[2] = parameters[0] ^ parameters[1]
        elif instruction == 0x1B:
            # onec

            registers[2] = (~parameters[0]) & 0xFFFF
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
                if len(hex(memory[parameters[0] + i])[2:]) < 2:
                    print("0" + hex(memory[parameters[0] + i])[2:], end = "", flush = True) 
                else:
                    print(hex(memory[parameters[0] + i])[2:], end = "", flush = True)
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
        elif instruction == 0xA7:
            # numstr

            number = str(parameters[2])
            padCount = 0

            for i in range(0, parameters[1]):
                if parameters[1] - i > len(number):
                    memory[parameters[0] + i] = 0
                    padCount += 1
                else:
                    memory[parameters[0] + i] = ord(number[i - padCount])
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

                file = open(fileDirectory, "wb")

                for i in range(0, parameters[1]):
                    file.write(bytes([memory[parameters[0] + i]]))

                file.close()

                registers[3] = 3
            else:
                registers[3] = 0
        elif instruction == 0xB3:
            # fwriter

            if fileDirectory != "":
                file = open(fileDirectory, "rb+")

                file.seek(parameters[2])

                for i in range(0, parameters[1]):
                    file.write(bytes([memory[parameters[0] + i]]))

                file.close()

                registers[3] = 3
            else:
                registers[3] = 0
        elif instruction == 0xB4:
            # fappend

            if fileDirectory != "":
                file = open(fileDirectory, "ab")

                for i in range(0, parameters[1]):
                    file.write(bytes([memory[parameters[0] + i]]))

                file.close()

                registers[3] = 3
            else:
                registers[3] = 0
        elif instruction == 0xB5:
            # fread

            if fileDirectory != "":
                file = open(fileDirectory, "rb")

                if parameters[0] + parameters[1] <= size:
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
                file = open(fileDirectory, "rb")

                file.seek(parameters[2])

                if parameters[0] + parameters[1] <= size:
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
        elif instruction == 0xB7:
            # fsize

            if fileDirectory != "":
                registers[1] = os.path.getsize(os.path.join(os.getcwd(), fileDirectory))
                registers[3] = 0
            else:
                registers[3] = 3
        elif instruction == 0xB8:
            # fdel

            if fileDirectory != "":
                try:
                    os.remove(os.path.join(os.getcwd(), fileDirectory))
                except:
                    pass
                
                registers[3] = 0
            else:
                registers[3] = 3
        elif instruction == 0xB9:
            # fmd

            directoryName = ""

            for i in range(0, parameters[1]):
                directoryName += chr(memory[parameters[0] + i])

            try:
                if not os.path.exists(os.path.join(os.getcwd(), directoryName)):
                    os.makedirs(os.path.join(os.getcwd(), directoryName))
            except:
                pass
        elif instruction == 0xBA:
            # frd

            directoryName = ""

            for i in range(0, parameters[1]):
                directoryName += chr(memory[parameters[0] + i])

            try:
                shutil.rmtree(os.path.join(os.getcwd(), directoryName))
            except:
                pass
        elif instruction == 0xBB:
            # fstart

            directoryName = ""

            for i in range(0, parameters[1]):
                directoryName += chr(memory[parameters[0] + i])

            directoryPath = directoryName
            directoryPosition = 0
        elif instruction == 0xBC:
            # fnext

            directoryListing = os.listdir(os.path.join(os.getcwd(), directoryPath))

            for i in range(0, 12):
                memory[parameters[0] + i] = 0
            
            if directoryPosition < len(directoryListing):
                filename = directoryListing[directoryPosition]

                for i in range(0, min(len(filename), 12)):
                    memory[parameters[0] + i] = ord(filename[i].upper())

            directoryPosition += 1
        elif instruction == 0xBD:
            # fex

            if fileDirectory != "":
                registers[1] = Path(os.path.join(os.getcwd(), fileDirectory)).exists()
                registers[3] = 0
            else:
                registers[3] = 3
        elif instruction == 0xBE:
            # fdir

            directoryListing = os.listdir(os.path.join(os.getcwd(), directoryPath))
            
            if directoryPosition < len(directoryListing):
                registers[1] = os.path.isdir(os.path.join(os.getcwd(), directoryPath, directoryListing[directoryPosition]))
            else:
                registers[1] = 0

            directoryPosition += 1
        elif instruction == 0xC0:
            # gpos

            registers[8] = parameters[0]
            registers[9] = parameters[1]
        elif instruction == 0xC1:
            # gsize

            registers[10] = parameters[0]
            registers[11] = parameters[1]
        elif instruction == 0xC2:
            # ginit

            drawtools.ginit(registers[10], registers[11])
        elif instruction == 0xC3:
            # gfill

            registers[3] = 6 - int(drawtools.gfill(parameters[0])) * 6
        elif instruction == 0xC4:
            # gpixel

            registers[3] = 6 - int(drawtools.gpixel(registers[8], registers[9], parameters[0])) * 6
        elif instruction == 0xC5:
            # gline

            registers[3] = 6 - int(drawtools.gline(registers[8], registers[9], registers[10], registers[11], parameters[0])) * 6
        elif instruction == 0xC6:
            # gfline

            registers[3] = 6 - int(drawtools.gfline(registers[8], registers[9], registers[10], registers[11], parameters[1], parameters[0])) * 6
        elif instruction == 0xC7:
            # grect

            if parameters[1] > 0:
                registers[3] = 6 - int(drawtools.grect(registers[8], registers[9], registers[10], registers[11], parameters[0], 0)) * 6
            else:
                registers[3] = 6 - int(drawtools.grect(registers[8], registers[9], registers[10], registers[11], parameters[0], 1)) * 6
        elif instruction == 0xC8:
            # gcircle

            if parameters[1] > 0:
                registers[3] = 6 - int(drawtools.gcircle(registers[8], registers[9], registers[10], parameters[0], 0)) * 6
            else:
                registers[3] = 6 - int(drawtools.gcircle(registers[8], registers[9], registers[10], parameters[0], 1)) * 6
        elif instruction == 0xC9:
            # gbin

            for i in range(0, parameters[2]):
                for j in range(0, len("{0:b}".format(memory[parameters[1] + i]))):
                    registers[3] = 6 - int(drawtools.gchar("{0:b}".format(memory[parameters[1] + i])[j], registers[8] + registers[8] + (j * registers[11] * 6), registers[9], registers[11], parameters[0])) * 6
        elif instruction == 0xCA:
            # gdec

            result = 0

            for i in range(0, parameters[2]):
                result = (result * 256) + memory[parameters[1] + i]

            for i in range(0, len(str(result))):
                registers[3] = 6 - int(drawtools.gchar(str(result)[i], registers[8] + (i * registers[11] * 6), registers[9], registers[11], parameters[0])) * 6
        elif instruction == 0xCB:
            # ghex

            for i in range(0, parameters[2]):
                if len(hex(memory[parameters[1] + i])[2:]) < 2:
                    registers[3] = 6 - int(drawtools.gchar("0", registers[8] + ((i * 2) * registers[11] * 6), registers[9], registers[11], parameters[0])) * 6
                    registers[3] = 6 - int(drawtools.gchar(hex(memory[parameters[1] + i])[2:], registers[8] + (((i * 2) + 1) * registers[11] * 6), registers[9], registers[11], parameters[0])) * 6
                else:
                    registers[3] = 6 - int(drawtools.gchar(hex(memory[parameters[1] + i])[2:][0], registers[8] + ((i * 2) * registers[11] * 6), registers[9], registers[11], parameters[0])) * 6
                    registers[3] = 6 - int(drawtools.gchar(hex(memory[parameters[1] + i])[2:][1], registers[8] + (((i * 2) + 1) * registers[11] * 6), registers[9], registers[11], parameters[0])) * 6
        elif instruction == 0xCC:
            # gasc

            for i in range(0, parameters[2]):
                registers[3] = 6 - int(drawtools.gchar(chr(memory[parameters[1] + i]), registers[8] + (i * registers[11] * 6), registers[9], registers[11], parameters[0])) * 6
        elif instruction == 0xCD:
            # gbmp

            fileDirectory = ""

            for i in range(0, parameters[1]):
                fileDirectory += chr(memory[parameters[0] + i])
            
            registers[3] = 6 - int(drawtools.gbmp(registers[8], registers[9], fileDirectory)) * 6
        elif instruction == 0xCE:
            # gtouch

            values = drawtools.gtouch(parameters[0] > 0)

            if values == False:
                registers[3] = 6
            else:
                registers[8] = values[0][0]
                registers[9] = values[0][1]
                registers[1] = values[1]

                registers[3] = 0
        elif instruction == 0xD0:
            # sleep

            time.sleep(parameters[0] / 1000)
        elif instruction == 0xD1:
            # gyear

            registers[1] = datetime.datetime.now().year
        elif instruction == 0xD2:
            # gmonth

            registers[1] = datetime.datetime.now().month
        elif instruction == 0xD3:
            # gdate

            registers[1] = datetime.datetime.now().day
        elif instruction == 0xD4:
            # gday

            registers[1] = datetime.datetime.now().weekday()
        elif instruction == 0xD5:
            # ghour

            registers[1] = datetime.datetime.now().hour
        elif instruction == 0xD6:
            # gminute

            registers[1] = datetime.datetime.now().minute
        elif instruction == 0xD7:
            # gsecond

            registers[1] = datetime.datetime.now().second
        elif instruction == 0xD8:
            # sdate
            # Skipping, system time shouldn't be easily set by programs

            pass
        elif instruction == 0xD9:
            # stime
            # Skipping, system time shouldn't be easily set by programs

            pass
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
        
        if instruction != 0x03 and instruction != 0x0B and instruction != 0x0C and instruction != 0x0D and instruction != 0x0E and instruction != 0x0F:
            # Only increase PC if jump instruction isn't used

            if instruction == 0xFD or instruction == 0xFE or instruction == 0xFF:
                # Jump by 4 in parameter instructions

                registers[0] += 4
            else:
                # Just jump by 1
                registers[0] += 1

    if debugging:
        output.returns(_("haltedEndMemoryDump", [" ".join(hex(i)[2:].zfill(2) for i in memory)]))
    else:
        output.returns(_("halted"))