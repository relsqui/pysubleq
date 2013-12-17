#!/usr/bin/python

import unittest, sys, contextlib

import subleq


class IOTrapper(object):
    def __init__(self):
        self._read_queue = ""
        self._write_queue = []
        self._pending_write = None

    def write(self, string):
        if self._pending_write:
            string = "".join([self._pending_write, string])
            self._write_queue.append(string)
            self._pending_write = None
        else:
            self._pending_write = string

    def empty_write(self):
        queue = self._write_queue
        self._write_queue = []
        return queue

    def readline(self):
        try:
            first_line, self._read_queue = self._read_queue.splitlines(True)
            return first_line
        except ValueError:
            raise StopIteration

    def readlines(self, sizehint):
        queue = self._read_queue.splitlines(True)
        self._read_queue = ""
        return queue

    def queue_read(self, string):
        self._read_queue = string

    def empty_read(self):
        queue = self._read_queue
        self._read_queue = ""
        return queue

    @contextlib.contextmanager
    def set_trap(self):
        real_stdout = sys.stdout
        real_stdin = sys.stdin
        try:
            sys.stdout = self
            sys.stdin = self
            yield
        finally:
            sys.stdout = real_stdout
            sys.stdin = real_stdin
        

class SubleqTests(unittest.TestCase):
    def setUp(self):
        subleq.memory = [0, 1, 2, 3, 4]

    def test_subleq_equal(self):
        inst = (4, 4, 5)
        pointer = subleq.subleq(*inst)
        self.assertEqual(pointer, 5)
        self.assertEqual(subleq.memory, [0, 1, 2, 3, 0])

    def test_subleq_negative(self):
        inst = (4, 3, 5)
        pointer = subleq.subleq(*inst)
        self.assertEqual(pointer, 5)
        self.assertEqual(subleq.memory, [0, 1, 2, -1, 4])

    def test_subleq_positive(self):
        inst = (3, 4, 5)
        pointer = subleq.subleq(*inst)
        self.assertIsNone(pointer)
        self.assertEqual(subleq.memory, [0, 1, 2, 3, 1])


    def test_normalize_short(self):
        old_inst = (0, 1)
        new_inst = subleq.normalize(old_inst, 0)
        self.assertEqual(new_inst, (0, 1, 1))

    def test_normalize_long(self):
        old_inst = (0, 1, 2)
        new_inst = subleq.normalize(old_inst, 0)
        self.assertEqual(old_inst, new_inst)


    def test_next_address_jump(self):
        pointer = subleq.next_address(1, 2)
        self.assertEqual(pointer, 1)

    def test_next_address_none(self):
        pointer = subleq.next_address(None, 2)
        self.assertEqual(pointer, 3)


    def test_parse_empty(self):
        fakeio = IOTrapper()
        with fakeio.set_trap():
            fakeio.queue_read("")
            program, errors = subleq.parse_program()
        self.assertEqual(errors, [])
        self.assertEqual(program, [])


if __name__ == '__main__':
    unittest.main()
