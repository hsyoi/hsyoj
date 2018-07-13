from django.test import TestCase

from common.judge import JudgeResult
from problems.models import Problem
from .models import Record


class RecordTest(TestCase):
    def setUp(self):
        super().setUpClass()

        # Prepare Problem
        example_problem = Problem.problem_set.create(
            title='A+B Problem',
            description="",

            input_file_name='input.in',
            output_file_name='output.out',

            stdio_flag=True,
        )
        for input_content, answer in [("1 1", "2"), ("13 8", "21")]:
            example_problem.testcase_set.create(
                input_content=input_content,
                answer_content=answer
            )

        # Prepare Source File
        source_file = 'tests/source/ac.c'
        with open(source_file) as f:
            self.source_code = f.read()
        compiler = 'gcc'

        # Generate Record
        self.record = Record(
            user=None,
            problem=example_problem,
            compiler=compiler,
            source_code=self.source_code,
            accepted_flag=True
        )

    def tearDown(self):
        self.record.delete()

    def test_record_generate(self):
        self.assertTrue(self.record.accepted_flag)
        self.assertEqual(self.record.source_code, self.source_code)
        self.assertEqual(self.record.compiler, 'gcc')

    def test_record_is_accepted_method(self):
        self.assertTrue(self.record.is_accepted())

    def test_record_get_result_method(self):
        self.assertEqual(self.record.get_result(), JudgeResult.AC)


class CompilationErrorRecordTest(TestCase):
    def setUp(self):
        super().setUpClass()

        # Prepare Problem
        example_problem = Problem.problem_set.create(
            title='A+B Problem',
            description="",

            input_file_name='input.in',
            output_file_name='output.out',

            stdio_flag=True,
        )
        for input_content, answer in [("1 1", "2"), ("13 8", "21")]:
            example_problem.testcase_set.create(
                input_content=input_content,
                answer_content=answer
            )

        # Prepare Source File
        source_file = 'tests/source/ce.cpp'
        with open(source_file) as f:
            self.source_code = f.read()
        compiler = 'g++'

        # Generate Record
        self.record = Record(
            user=None,
            problem=example_problem,
            compiler=compiler,
            source_code=self.source_code,
            accepted_flag=False
        )
        self.record.testcaseresult_set.create(
            result_code=JudgeResult.CE.value,
            test_case=None,
        )

    def tearDown(self):
        self.record.delete()

    def test_record_generate(self):
        self.assertFalse(self.record.accepted_flag)
        self.assertEqual(self.record.source_code, self.source_code)
        self.assertEqual(self.record.compiler, 'g++')

    def test_record_is_accepted(self):
        self.assertFalse(self.record.is_accepted())

    def test_record_get_result(self):
        self.assertEqual(self.record.get_result(), JudgeResult.CE)
