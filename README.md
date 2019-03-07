# LiveG Assembler
Compiler and runtime used to assemble LiveG Assembly (*.gas, *.gbn) files.

This repository is licensed by the [LiveG Open-Source Licence](https://github.com/LiveG-Development/Assembler/blob/master/LICENCE.md).

## Assembler instructions
| Instruction   | Code  | Description                                   | Parameters                                        |
|---------------|-------|-----------------------------------------------|---------------------------------------------------|
| halt          | 0x00  | Halts the execution of the program.           |                                                   |
| allocate      | 0x01  | Allocates/clears memory at address.           | startAddr (uint), length (uint)                   |
| copy          | 0x02  | Copies a block of memory at address.          | startAddr (uint), length (uint), newAddr (uint)   |
| jump          | 0x03  | Jumps PC to address.                          | addr (uint)                                       |
| write         | 0x04  | Writes ubyte to memory at address.            | value (ubyte), addr (uint)                        |
| read          | 0x05  | Reads ubyte memory at address to RM.          | addr (uint)                                       |
| add           | 0x06  | Adds two parameters and stores in AR.         | firstVal (uint), secondVal (uint)                 |
| sub           | 0x07  | Subtracts two parameters and store it in AR.  | firstVal (uint), secondVal (uint)                 |
| mul           | 0x08  | Multiplies two parameters and stores in AR.   | firstVal (uint), secondVal (uint)                 |
| div           | 0x09  | Divides two parameters and stores in AR.      | firstVal (uint), secondVal (uint)                 |
| mod           | 0x0A  | Modulos two parameters and stores in AR.      | firstVal (uint), secondVal (uint)                 |
| equ           | 0x0B  | Jumps to address if values are equal.         | firstVal (uint), secondVal (uint), addr (uint)    |
| neq           | 0x0C  | Jumps to address if values are not equal.     | firstVal (uint), secondVal (uint), addr (uint)    |
| ltn           | 0x0D  | Jumps to address if values are less than.     | firstVal (uint), secondVal (uint), addr (uint)    |
| gtn           | 0x0E  | Jumps to address if values are greater than.  | firstVal (uint), secondVal (uint), addr (uint)    |
| func          | 0x0F  | Executes function at address.                 | addr (uint)                                       |
| ret           | 0x10  | Returns from function to original address.    |                                                   |
| sreg          | 0x11  | Sets register by its index.                   | index (uint), value (uint)                        |
| sgp           | 0x12  | Sets general-purpose register by its index.   | index (uint), value (uint)                        |
| cgp           | 0x13  | Clears all general-purpose registers.         |                                                   |
| dwrite        | 0x14  | Writes uint to memory at address.             | value (uint), addr (uint)                         |
| dread         | 0x15  | Reads uint memory at address to RM register.  | addr (uint)                                       |
| outbin        | 0xA0  | Writes output of memory to TTY in binary.     | startAddr (uint), length (uint)                   |
| outdec        | 0xA1  | Writes output of ubyte in decimal.            | startAddr (uint), length (uint)                   |
| outhex        | 0xA2  | Writes output of ubyte in hexadecimal.        | startAddr (uint), length (uint)                   |
| outasc        | 0xA3  | Writes output of ubyte in ASCII.              | startAddr (uint), length (uint)                   |
| in            | 0xA4  | Gets input and stores it as ASCII in address. | startAddr (uint), length (uint)                   |
| len           | 0xA5  | Gets length of memory ubyte and stores in RM. | startAddr (uint), char (ubyte)                    |
| strnum        | 0xA6  | Gets number from string and stores in RM.     | startAddr (uint), length (uint)                   |
| fopen         | 0xB0  | Opens file at directory string.               | startAddr (uint), length (uint)                   |
| fclose        | 0xB1  | Closes currently open file.                   |                                                   |
| fwrite        | 0xB2  | Writes memory into file at position.          | startAddr (uint), length (uint)                   |
| fwriter       | 0xB3  | Writes memory into file in range.             | startAddr (uint), length (uint), fileAddr (uint)  |
| fappend       | 0xB4  | Appends memory to file at position.           | startAddr (uint), length (uint)                   |
| fread         | 0xB5  | Reads file into memory at position.           | startAddr (uint), length (uint)                   |
| freadr        | 0xB6  | Reads file into memory in range.              | startAddr (uint), length (uint), fileAddr (uint)  |
| fsize         | 0xB7  | Gets size of file and stores in RM.           |                                                   |
| (setpar)      | 0xFD  | Sets parameter to value.                      | param (uint), value (any)                         |
| (regpar)      | 0xFE  | Loads register into parameter.                | param (uint), regIndex (uint)                     |
| (loadpar)     | 0xFF  | Loads memory address into parameter.          | param (uint), addr (uint)                         |

## Registers
| Register      | Description                                   | Index |
|---------------|-----------------------------------------------|-------|
| PC            | Program counter, current program position.    | 0     |
| RM            | Read-memory register, result of memory read.  | 1     |
| AR            | Arithemtic result register, result of calc.   | 2     |
| ER            | Error register, for errors from instructions. | 3     |
| FR            | Function register, for initiated instruction. | 4     |
| PM (1-3)      | Parameter register, for next instruction.     | 5-7   |
| GX            | Graphics X position register.                 | 8     |
| GY            | Graphics Y position register.                 | 9     |
| GW            | Graphics width register.                      | 10    |
| GH            | Graphics height register.                     | 11    |
| GP (1-8)      | General-purpose registers.                    | 12-19 |

## Error codes
Error codes are collected from ER, and are set to 0 by running any arithmetic
calculation that doesn't produce an error.

| Error Code    | Description                                   |
|---------------|-----------------------------------------------|
| 0             | No error.                                     |
| 1             | Division or modulus by 0.                     |
| 2             | String is not a number.                       |
| 3             | File is not open.                             |
| 4             | File cannot be further read.                  |
| 5             | File cannot fit in memory.                    |