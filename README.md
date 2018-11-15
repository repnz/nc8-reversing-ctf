# NC8 Mainframe Management Interface

Hi! 

This is a reverse engineering ctf from ringzer0team.com.
The purpose of this ctf is to research and reverse engineer binaries from a remote machine with an unknown architecture.

## Machine

- The CPU has 16 regs (specified in the manual)
- lr - the link register is r13
- the machine is big endian -> from the nature of addresses in the example program
- the size of registers is 16 bit 
- RISC architecture
- 16 instructions

## Instructions

- Every opcode is a single byte
- the first nibble is the operation, second is the argument
- known instructions:
	- 00 int 
	- 10 mov reg, imm
	- 20 mov [reg], reg
	- 30 mov reg, [reg]
	- 40 add reg, reg 
	- 50 xor 
	- 60 add  
	- 70 or 
	- 80 mul
	- 90 div
	- a0 jz offset
	- b0 ??
	- c0 jmp offset
	- d0 push reg
	- e0 push [offset]
	- f0 pop reg

The conclusion that the first nibble indicates the operation was deduced from:
- the example and the part_1 code,
- there are 16 instructions so it seems legit to encode the instruction in the first nibble


### 00 int:

int 0 -> exit
int 1 -> read char
int 2 -> write char
int 4 -> unknown

usage is mainly in the read() and write() functions. those functions are the same all the time

### 10 mov reg, imm

Usage in example:

1B mov r2, -1
1D mov r3,  1

Those minimal examples cannot teach a lot.

Usage in part_1:

11 mov r0, 1 - before returning from func

- After writing an assembler and running code on the server, 
I learned the imm is limited to this mapping:

```python
 self.imm_repr_to_imm = {
            0b11: -1,
            0b10: 2,
            0b00: -2,
            0b01: 1
        }
```

### 20 mov [reg], reg

Single usage in read() function to move the char from r0 to [r1] -> 24


### 30 mov reg, [reg]

Read byte from the register memory, the high values of the reg will be zero.
How do we know its a single byte? part 1 has shown us with the read and substruct.
Usage in examples:

31 mov r0, [r1]

Usage in part 1:

36 mov r1, [r2]

deduced from the fact that a read from the array needs to exist in that code seq. 

### 40 add reg, reg

example

47 add r1, r2
42 add r0, r2

part 1
4b add r2, r3
41 add r0, r1

### 50 xor instruction

- first usage was in part_1, zeroing r0 like this:

50 zero r0

- when saw the usage in part_2, it was clear it is not a zero instruction:

5f zero sp (??)

so, after some research I thought it was a sub instruction:

5f sub r3, r3 (to clear r3)
53 sub r0, r3 (an operation that helps checking if r0 equals r3)

but then, when reversing some() and some2() i learned that 0x100..0x104 has to equal 0xfa..0xfe after the some() operation with the input, so i took the word 'FLAG' that returned True in some2(), and look was operation it was doing, it was xor.

So 0x50 is a xor operation, i can say for sure now.

### 90 div reg, reg instruction

I thought it was a xchg instruction, but no.

the div instruction divides the dst reg by the src reg and stores the reminder on the (src reg/r1). 
maybe the result of the div is stored in the dst operand, not known yet.

first usage: part 2 

0x99 div r2, r1

after running div on the server, the speculation was correct.

### 70 Unknown Operation

This unknown operation happened at the end of part 2 before printing CODE ACCEPTED. 
my speculation is that it is a math operation between r3, r3.


# E0 
00 -> int 0
02 -> int 2
FE -> pop pc
E0 -> push [._start]
00 25 -> .start -> big endian
F1 -> pop r1
F0 -> pop r0
DD -> push lr
E9 -> push -7
EC -> push -4
ED -> push -3
E0 -> push +1
A6 -> jz +6
   -> jz +1

positive = 2+x
neg      = 0xf-x
push minus -> 0xF0 - offset
push plus ->  0xE0 + 
stack is 16 bit

jz -> jumps to zero if r0 is zero
int 2 > print char from r0
int 0 -> exit
lr -> where did you come from my friend