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
errors = []

for line in fileinput.input():
    if line[0] in ["\n", "#"]:
        # Ignore blank lines and comments.
        pass
    elif not memory:
        # The first non-blank non-comment line initializes memory.
        try:
            memory = map(int, line.split())
        except ValueError as e:
            errors.append((fileinput.filename(), fileinput.filelineno(), str(e), line))
    else:
        # The rest are sets of operands for subleq.
        try:
            operands = tuple(map(int, line.split()))
            if len(operands) == 1:
                raise ValueError("not enough operands (expected 2 or 3)")
            elif len(operands) > 3:
                raise ValueError("too many operands (expected 2 or 3)")
            for operand in operands[:2]:
                if operand not in xrange(len(memory)):
                    raise ValueError("register {} out of range (max {})".format(operand, len(memory)-1))
            program.append(operands)
        except ValueError as e:
            errors.append((fileinput.filename(), fileinput.filelineno(), str(e), line))

if errors:
    error_lines = []
    for filename, lineno, message, line in errors:
        error_lines.append('Error: "{}" line {}: {}:\n{}'.format(filename, lineno, message, line.strip()))
    print "\n\n".join(error_lines)
else:
    run(program)
    print memory
