from django.test import TestCase

from problems.models import Problem

from .models import Record


class RecordTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

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

    def test_record_generate(self):
        source_file = 'tests/source/ac.c'
        with open(source_file) as f:
            source_code = f.read()
        compiler = 'gcc'

        record = Record.generate(
            user=None,
            problem=self.example_problem,
            compiler=compiler,
            source_code=source_code,
        )

        self.assertTrue(record.accepted_flag)
        self.assertEqual(record.source_code, source_code)
        self.assertEqual(record.compiler, 'gcc')

    def test_record_is_accpeted(self):
        pass

    def test_record_get_result(self):
        pass
