"""Test compilers."""
# TODO: Add tests with error status
import difflib
import os
import subprocess
import unittest

from hsyoj.common.compiler import CompileResult, get_compiler
from hsyoj.common.judge import diff_bytes


class CCompilerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.compiler = get_compiler('c')
        cls.source = os.path.abspath("tests/source/ac.c")
        cls.ce_source = os.path.abspath("tests/source/ce.c")
        with open(cls.source) as f:
            cls.code = f.read()
        cls.binary = '/tmp/binaryC'

    def tearDown(self):
        try:
            os.remove(self.binary)
        except FileNotFoundError:
            pass

    def test_compile_code(self):
        self.compiler.compile_code(self.code, self.binary)
        process = subprocess.run(
            self.binary, input=b"18 23", stdout=subprocess.PIPE)
        answer = process.stdout
        expect = b"41\n"
        self.assertFalse(diff_bytes(answer, expect))

    def test_compile_source(self):
        self.compiler.compile_file(self.source, self.binary)
        process = subprocess.run(
            self.binary, input=b"18 23", stdout=subprocess.PIPE)
        answer = process.stdout
        expect = b"41\n"
        self.assertFalse(diff_bytes(answer, expect))

    def test_compile_error(self):
        assert self.compiler.compile_file(
            self.ce_source, self.binary) is CompileResult.CE


class CppCompilerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.compiler = get_compiler('cpp')
        cls.source = os.path.abspath("tests/source/ac.cpp")
        cls.ce_source = os.path.abspath("tests/source/ce.cpp")
        with open(cls.source) as f:
            cls.code = f.read()
        cls.binary = "/tmp/binaryCpp"

    def tearDown(self):
        try:
            os.remove(self.binary)
        except FileNotFoundError:
            pass

    def test_compile_code(self):
        self.compiler.compile_code(self.code, self.binary)
        process = subprocess.run(
            self.binary, input=b"18 23", stdout=subprocess.PIPE)
        answer = process.stdout
        expect = b"41\n"
        self.assertFalse(diff_bytes(answer, expect))

    def test_compile_source(self):
        self.compiler.compile_file(self.source, self.binary)
        process = subprocess.run(
            self.binary, input=b"18 23", stdout=subprocess.PIPE)
        answer = process.stdout
        expect = b"41\n"
        self.assertFalse(diff_bytes(answer, expect))

    def test_compile_error(self):
        assert self.compiler.compile_file(
            self.ce_source, self.binary) is CompileResult.CE


if __name__ == '__main__':
    unittest.main()
