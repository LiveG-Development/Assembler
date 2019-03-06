# LiveG Assembler
# 
# Copyright (C) LiveG. All Rights Reserved.
# Copying is not a victimless crime. Anyone caught copying LiveG software may
# face sanctions.
# 
# https://liveg.tech
# Licensed by the LiveG Open-Source Licence, which can be found at LICENCE.md.

registers = [0] * 8
memory = [0] * 6144

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
        
        memory[parameters[1]] = parameters[0]
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
    elif instruction == 0xA0:
        # outbin

        for i in range(0, parameters[1]):
            print("{0:b}".format(memory[parameters[0] + i]), end = "", flush = True)
    elif instruction == 0xA1:
        # outdec

        result = 0

        for i in range(0, parameters[1]):
            result += memory[parameters[0] + i]

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