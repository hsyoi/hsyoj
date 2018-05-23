"""Test judge."""
import os
import unittest

from hsyoj.common.judge import JudgeResult, judge


class JudgeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c_source = os.path.abspath('tests/source/ac.c')
        cls.cpp_source = os.path.abspath('tests/source/ac.cpp')
        cls.test_cases = [(
            os.path.abspath('tests/data/0.in'),
            os.path.abspath('tests/data/0.ans')
        ), (
            os.path.abspath('tests/data/1.in'),
            os.path.abspath('tests/data/1.ans')
        ),
        ]

    def test_judge_c(self):
        with open(self.c_source) as f:
            source_code = f.read()
        results = judge(language='c', source_code=source_code, test_cases=self.test_cases,
                        input_file='input.in', output_file='output.out', stdio=True)
        self.assertListEqual(results, [JudgeResult.AC, JudgeResult.AC])

    def test_judge_cpp(self):
        with open(self.cpp_source) as f:
            source_code = f.read()
        results = judge(language='cpp', source_code=source_code, test_cases=self.test_cases,
                        input_file='input.in', output_file='output.out', stdio=True)
        self.assertListEqual(results, [JudgeResult.AC, JudgeResult.AC])

    # TODO: Add tests with wrong status


if __name__ == '__main__':
    unittest.main()
