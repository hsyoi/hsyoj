from django.test import TestCase

from common.judge import JudgeResult
from problems.models import Problem

from .generator import generate


class RecordTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Prepare Problem
        cls.example_problem = Problem.problem_set.create(
            title='A+B Problem',
            description="",

            input_file_name='input.in',
            output_file_name='output.out',

            stdio_flag=True,
        )
        for input_content, answer in [("1 1", "2"), ("13 8", "21")]:
            cls.example_problem.testcase_set.create(
                input_content=input_content,
                answer_content=answer
            )

        # Prepare Source File
        source_file = 'tests/source/ac.c'
        with open(source_file) as f:
            cls.source_code = f.read()
        compiler = 'gcc'

        # Generate Record
        cls.record = generate(
            user=None,
            problem=cls.example_problem,
            compiler=compiler,
            source_code=cls.source_code,
        )

    def test_record_generate(self):
        self.assertTrue(self.record.accepted_flag)
        self.assertEqual(self.record.source_code, self.source_code)
        self.assertEqual(self.record.compiler, 'gcc')

    def test_record_is_accpeted(self):
        self.assertTrue(self.record.is_accepted())

    def test_record_get_result(self):
        self.assertEqual(self.record.get_result(), JudgeResult.AC)


class CompilationErrorRecordTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Prepare Problem
        cls.example_problem = Problem.problem_set.create(
            title='A+B Problem',
            description="",

            input_file_name='input.in',
            output_file_name='output.out',

            stdio_flag=True,
        )
        for input_content, answer in [("1 1", "2"), ("13 8", "21")]:
            cls.example_problem.testcase_set.create(
                input_content=input_content,
                answer_content=answer
            )

        # Prepare Souce File
        source_file = 'tests/source/ce.cpp'
        with open(source_file) as f:
            cls.source_code = f.read()
        compiler = 'g++'

        # Generate Record
        cls.record = generate(
            user=None,
            problem=cls.example_problem,
            compiler=compiler,
            source_code=cls.source_code,
        )

    def test_record_generate(self):
        self.assertFalse(self.record.accepted_flag)
        self.assertEqual(self.record.source_code, self.source_code)
        self.assertEqual(self.record.compiler, 'g++')

    def test_record_is_accpeted(self):
        self.assertFalse(self.record.is_accepted())

    def test_record_get_result(self):
        self.assertEqual(self.record.get_result(), JudgeResult.CE)
