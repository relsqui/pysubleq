#!/usr/bin/python

import fileinput


def subleq(a, b, c):
    global memory
    memory[b] -= memory[a]
    if memory[b] <= 0:
        return c
    return None

def normalize(instruction, pointer):
    if len(instruction) < 3:
        instruction = instruction + (pointer + 1,)
    return instruction

def next_address(jump, pointer):
    if jump is not None:
        return jump
    return pointer + 1

def run(program):
    pointer = 0
    while pointer >= 0 and pointer < len(program):
        instruction = program[pointer]
        print memory
        print instruction
        a, b, c = normalize(instruction, pointer)
        pointer = next_address(subleq(a, b, c), pointer)


memory = []
program = []

for line in fileinput.input():
    if line[0] in ["\n", "#"]:
        # Ignore blank lines and comments.
        pass
    elif not memory:
        # The first non-blank non-comment line initializes memory.
        memory = map(int, line.split())
    else:
        # The rest are sets of operands for subleq.
        program.append(tuple(map(int, line.split())))

run(program)
print memory
