subleq
------
The single instruction of this processor is subleq: "subtract, and branch if less than or equal to zero." Its operands are three memory addresses (a, b, c). For each instruction, subleq subtracts the value at address a from the value at address b, and stores the result at address b. If that result is negative, execution jumps to address c; otherwise it proceeds to the next instruction. If c is omitted, execution always proceeds to the next instruction.

programs
--------
pysubleq programs have separate data and instruction memory. The first line in a pysubleq program file may have any amount of integers in it, separated by spaces, and is used to initialize the data registers. All following lines are taken as sets of operands to the subleq operator. Blank lines and lines starting with # are ignored. Example:


```
2 5 0

0 2
2 1
2 2
```

This program initializes the memory registers to [2, 5, 0], and then performs the subleq operation three times: on registers 0 and 2, then 2 and 1, then 2 and 2.

pysubleq reads programs from stdin or any filenames you specify. If the above example was in a file called `add`, you could do `subleq.py add` and get this:

```
[2, 5, 0]
(0, 2)
[2, 5, -2]
(2, 1)
[2, 7, -2]
(2, 2)
[2, 7, 0]
```

For each instruction executed, pysubleq shows the memory state before and after as well as the operands for that instruction. The example program has added the value in register 0 to the value in register 1.
