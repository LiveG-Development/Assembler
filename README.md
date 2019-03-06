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
| read          | 0x05  | Reads ubyte memory at address to RM register. | addr (uint)                                       |
| add           | 0x06  | Add two parameters and store it in AR.        | firstVal (uint), secondVal (uint)                 |
| sub           | 0x07  | Subtract two parameters and store it in AR.   | firstVal (uint), secondVal (uint)                 |
| mul           | 0x08  | Multiply two parameters and store it in AR.   | firstVal (uint), secondVal (uint)                 |
| div           | 0x09  | Divide two parameters and store it in AR.     | firstVal (uint), secondVal (uint)                 |
| mod           | 0x0A  | Modulo of two parameters and store it in AR.  | firstVal (uint), secondVal (uint)                 |
| equ           | 0x0B  | Jump to address if values are equal.          | firstVal (uint), secondVal (uint), addr (uint)    |
| neq           | 0x0C  | Jump to address if values are not equal.      | firstVal (uint), secondVal (uint), addr (uint)    |
| ltn           | 0x0D  | Jump to address if values are less than.      | firstVal (uint), secondVal (uint), addr (uint)    |
| gtn           | 0x0E  | Jump to address if values are greater than.   | firstVal (uint), secondVal (uint), addr (uint)    |
| func          | 0x0F  | Execute function at address.                  | addr (uint)                                       |
| ret           | 0x10  | Return from function to original address.     |                                                   |
| dwrite        | 0x14  | Writes uint to memory at address.             | value (uint), addr (uint)                         |
| dread         | 0x15  | Reads uint memory at address to RM register.  | addr (uint)                                       |
| outbin        | 0xA0  | Writes output of memory to TTY in binary.     | startAddr (uint), length (uint)                   |
| outdec        | 0xA1  | Writes output of ubyte in decimal.            | startAddr (uint), length (uint)                   |
| outhex        | 0xA2  | Writes output of ubyte in hexadecimal.        | startAddr (uint), length (uint)                   |
| outasc        | 0xA3  | Writes output of ubyte in ASCII.              | startAddr (uint), length (uint)                   |
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

## Error codes
Error codes are collected from ER, and are set to 0 by running any arithmetic
calculation that doesn't produce an error.

| Error Code    | Description                                   |
|---------------|-----------------------------------------------|
| 0             | No error.                                     |
| 1             | Division or modulus by 0.                     |