"""Test judge."""
import os
import unittest

from common.judge import JudgeResult, judge


class JudgeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c_source_file = os.path.abspath('tests/source/ac.c')
        cls.cpp_source_file = os.path.abspath('tests/source/ac.cpp')
        cls.test_cases = [
            (
                "1 1",
                "2"
            ),
            (
                "13 8",
                "21"
            ),
        ]

    def test_judge_c(self):
        with open(self.c_source_file) as f:
            source_code = f.read()
        results = judge(
            source_code=source_code,
            language_suffix='.c',
            test_cases=self.test_cases,
            input_file_name='input.in',
            output_file_name='output.out',
            stdio_flag=True
        )
        self.assertListEqual(results, [JudgeResult.AC, JudgeResult.AC])

    def test_judge_cpp(self):
        with open(self.cpp_source_file) as f:
            source_code = f.read()
        results = judge(
            source_code=source_code,
            language_suffix='.cpp',
            test_cases=self.test_cases,
            input_file_name='input.in',
            output_file_name='output.out',
            stdio_flag=True
        )
        self.assertListEqual(results, [JudgeResult.AC, JudgeResult.AC])

    # TODO: Add tests with wrong status


if __name__ == '__main__':
    unittest.main()
