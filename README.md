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
| outbin        | 0xA0  | Writes output of ubyte to TTY in binary.      | startAddr (uint), length (uint)                   |
| outdec        | 0xA1  | Writes output of ubyte in decimal.            | startAddr (uint), length (uint)                   |
| outhex        | 0xA2  | Writes output of ubyte in hexadecimal.        | startAddr (uint), length (uint)                   |
| outasc        | 0xA3  | Writes output of ubyte in ASCII.              | startAddr (uint), length (uint)                   |
| in            | 0xA4  | Gets input and stores it as ASCII in address. | startAddr (uint), length (uint)                   |
| len           | 0xA5  | Gets length of memory ubyte and stores in RM. | startAddr (uint), char (ubyte)                    |
| strnum        | 0xA6  | Gets number from string and stores in RM.     | startAddr (uint), length (uint)                   |
| numstr        | 0xA7  | Stores number in memory as string.            | startAddr (uint), length (uint), value (uint)     |
| fopen         | 0xB0  | Opens file at directory string.               | startAddr (uint), length (uint)                   |
| fclose        | 0xB1  | Closes currently open file.                   |                                                   |
| fwrite        | 0xB2  | Writes memory into file at position.          | startAddr (uint), length (uint)                   |
| fwriter       | 0xB3  | Writes memory into file in range.             | startAddr (uint), length (uint), fileAddr (uint)  |
| fappend       | 0xB4  | Appends memory to file at position.           | startAddr (uint), length (uint)                   |
| fread         | 0xB5  | Reads file into memory at position.           | startAddr (uint), length (uint)                   |
| freadr        | 0xB6  | Reads file into memory in range.              | startAddr (uint), length (uint), fileAddr (uint)  |
| fsize         | 0xB7  | Gets size of file and stores in RM.           |                                                   |
| fdel          | 0xB8  | Closes and deletes open file.                 |                                                   |
| fmd           | 0xB9  | Creates directory with name.                  | startAddr (uint), length (uint)                   |
| frd           | 0xBA  | Deletes directory with name.                  | startAddr (uint), length (uint)                   |
| fstart        | 0xBB  | Opens directory for listing.                  | startAddr (uint), length (uint)                   |
| fnext         | 0xBC  | Gets next file in directory and stores name.  | nameAddr (uint)                                   |
| fex           | 0xBD  | Checks if open file exists and stores in RM.  |                                                   |
| fdir          | 0xBE  | Checks if next file is directory into RM.     |                                                   |
| gpos          | 0xC0  | Sets GX and GY registers to values.           | xValue (uint), yValue (uint)                      |
| gsize         | 0xC1  | Sets GW and GH registers to values.           | wValue (uint), hValue (uint)                      |
| ginit         | 0xC2  | Sets drawing area.                            |                                                   |
| gfill         | 0xC3  | Fills screen with colour.                     | colour (uint)                                     |
| gpixel        | 0xC4  | Draws pixel.                                  | colour (uint)                                     |
| gline         | 0xC5  | Draws line.                                   | colour (uint)                                     |
| gfline        | 0xC6  | Draws fast line.                              | colour (uint), isVertical (bool)                  |
| grect         | 0xC7  | Draws rectangle.                              | colour (uint), isFilled (bool)                    |
| gcircle       | 0xC8  | Draws circle.                                 | colour (uint), isFilled (bool)                    |
| gbin          | 0xC9  | Draws output of ubyte in binary.              | colour (uint), startAddr (uint), length (uint)    |
| gdec          | 0xCA  | Draws output of ubyte in decimal.             | colour (uint), startAddr (uint), length (uint)    |
| ghex          | 0xCB  | Draws output of ubyte in hexadecimal.         | colour (uint), startAddr (uint), length (uint)    |
| gasc          | 0xCC  | Draws output of ubyte in ASCII.               | colour (uint), startAddr (uint), length (uint)    |
| gbmp          | 0xCD  | Draws bitmap by string.                       | startAddr (uint), length (uint)                   |
| gtouch        | 0xCE  | Gets touch and stores in GX, GY and RM.       | waitForPress (bool)                               |
| sleep         | 0xD0  | Sleep for a specified period of milliseconds. | milliseconds (uint)                               |
| gyear         | 0xD1  | Gets the current year and stores in RM.       |                                                   |
| gmonth        | 0xD2  | Gets the current month and stores in RM.      |                                                   |
| gdate         | 0xD3  | Gets the current month date and stores in RM. |                                                   |
| gday          | 0xD4  | Gets the current weekday and stores in RM.    |                                                   |
| ghour         | 0xD5  | Gets the current hour and stores in RM.       |                                                   |
| gmin          | 0xD6  | Gets the current minute and stores in RM.     |                                                   |
| gsec          | 0xD7  | Gets the current second and stores in RM.     |                                                   |
| sdate         | 0xD8  | Sets the current date.                        | date (uint), month (uint), year (uint)            |
| stime         | 0xD9  | Sets the current time.                        | hour (uint), min (uint), sec (uint)               |
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
| 6             | Cannot draw on non-existent display.          |