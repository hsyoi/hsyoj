import uuid

from django.db import models

from common.compiler import SUPPORTED_COMPILERS, SUPPORTED_LANGUAGE_SUFFIXES
from common.judge import JudgeResult, judge


class Record(models.Model):
    record_set = models.Manager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        editable=False,
    )
    problem = models.ForeignKey(
        "problems.Problem",
        on_delete=models.SET_NULL,
        null=True,
        editable=False,
    )
    compiler = models.CharField(
        max_length=4,
        choices=SUPPORTED_COMPILERS,
        editable=False,
    )
    accepted_flag = models.BooleanField(editable=False)
    source_code = models.TextField(editable=False)
    submit_time = models.DateTimeField(auto_now_add=True, editable=False)
    # TODO Add running time and memory cost
    # running_time = models.DurationField(editable=False)
    # memory_cost = models. ...

    class Meta:
        permissions = (
            ('view_all_records', "View all records."),
        )

    # TODO Rewrite this method
    @classmethod
    def generate(cls, user, problem, compiler, source_code):
        user = None  # TODO Get a user and save it?
        judge_arguments = problem.get_problem_config()
        judge_arguments['source_code'] = source_code
        judge_arguments['language_suffix'] = \
            SUPPORTED_LANGUAGE_SUFFIXES[compiler][0]
        judge_results = judge(**judge_arguments)
        assert judge_results, "Error, judge results should never be empty."

        accepted_flag = all(
            map(lambda result: result.value == 0, judge_results))

        record = cls.record_set.create(
            user=user,
            problem=problem,
            compiler=compiler,
            source_code=source_code,
            accepted_flag=accepted_flag,
            # TODO Add running time and memory cost
            # running_time = models.DurationField(editable=False)
            # memory_cost = models. ...
        )

        if judge_results[0] is not JudgeResult.CE:
            for judge_result, test_case in zip(judge_results,
                                               problem.testcase_set.all()
                                               ):
                record.testcaseresult_set.create(
                    result_code=judge_result.value,
                    test_case=test_case,
                )

        return record

    def get_result(self) -> JudgeResult:
        if self.is_accepted():
            return JudgeResult.AC
        for result in self.testcaseresult_set:
            if result.result_code != 0:
                return JudgeResult(result.result_code)

        raise RuntimeError("All test case results in the record is AC.",
                           "But the accepted_flag is False!")

    def is_accepted(self) -> bool:
        return self.accepted_flag
    is_accepted.admin_order_field = 'Accepted'
    is_accepted.boolean = True
    is_accepted.short_description = 'Is accepted'


class TestCaseResult(models.Model):
    result_code = models.SmallIntegerField(editable=False)
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    test_case = models.ForeignKey(
        "problems.TestCase",
        on_delete=models.CASCADE
    )
