#!/usr/bin/python

import fileinput

def subleq(a, b, c):
    global memory
    memory[b] -= memory[a]
    if memory[b] <= 0:
        return c
    return None

def run(program):
    global memory
    pointer = 0
    while pointer >= 0 and pointer < len(program):
        instruction = program[pointer]
        print memory
        print instruction

        if len(instruction) < 3:
            instruction = instruction + (pointer + 1,)
        a, b, c = instruction

        newpointer = subleq(a, b, c)
        if newpointer is None:
            pointer += 1
        else:
            pointer = newpointer


memory = []
program = []

for line in fileinput.input():
    # The first line of the file is starting memory.
    # The rest are sets of operands. Blank lines are ignored.
    if line == "\n":
        continue
    if fileinput.isfirstline():
        memory = map(int, line.split())
    else:
        program.append(tuple(map(int, line.split())))

run(program)
print memory
