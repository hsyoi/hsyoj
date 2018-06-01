# TODO: Add tests with error status
import os
import subprocess
import tempfile
import unittest

from common.compiler import get_compiler
from common.judge import diff_bytes


class CompilerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skipTest(cls, "Base test case")

    def test_compile_source_code(self):
        self.compiler.compile_source_code_to(
            self.source_code,
            self.executing_file
        )
        process = subprocess.run(
            self.executing_file,
            input=self.test_input,
            stdout=subprocess.PIPE
        )
        result = process.stdout
        self.assertFalse(
            diff_bytes(
                result,
                self.test_answer
            )
        )

    def test_compile_source_file(self):
        self.compiler.compile_source_file_to(
            self.source_file,
            self.executing_file
        )
        process = subprocess.run(
            self.executing_file,
            input=self.test_input,
            stdout=subprocess.PIPE
        )
        result = process.stdout
        self.assertFalse(
            diff_bytes(
                result,
                self.test_answer
            )
        )

    def test_compile_error(self):
        with self.assertRaises(subprocess.CalledProcessError):
            self.compiler.compile_source_file_to(
                self.compile_error_source_file,
                self.executing_file
            )


class CCompilerTest(CompilerTest):
    @classmethod
    def setUpClass(cls):
        cls.compiler = get_compiler('gcc')
        cls.source_file = os.path.abspath("tests/source/ac.c")
        cls.compile_error_source_file = os.path.abspath("tests/source/ce.c")
        cls.test_input = b'13 29'
        cls.test_answer = b'42'
        with open(cls.source_file) as f:
            cls.source_code = f.read()
        cls.executing_file = os.path.join(
            tempfile.gettempdir(),
            'binary_c.exe'
        )

    def tearDown(self):
        try:
            os.remove(self.executing_file)
        except FileNotFoundError:
            pass


class CppCompilerTest(CompilerTest):
    @classmethod
    def setUpClass(cls):
        cls.compiler = get_compiler('g++')
        cls.source_file = os.path.abspath("tests/source/ac.cpp")
        cls.compile_error_source_file = os.path.abspath("tests/source/ce.cpp")
        cls.test_input = b'13 29'
        cls.test_answer = b'42'
        with open(cls.source_file) as f:
            cls.source_code = f.read()
        cls.executing_file = os.path.join(
            tempfile.gettempdir(),
            'binary_cpp.exe'
        )

    def tearDown(self):
        try:
            os.remove(self.executing_file)
        except FileNotFoundError:
            pass


if __name__ == '__main__':
    unittest.main()
