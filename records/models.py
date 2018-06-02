from django.db import models
from django.utils.timezone import datetime

from common.compiler import SUPPORTED_COMPILERS
from common.judge import JudgeResult, judge


class Record(models.Model):
    records_set = models.Manager()

    user = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        editable=False
    )
    problem = models.ForeignKey(
        "problems.Problem",
        on_delete=models.SET_NULL,
        null=True,
        editable=False
    )
    language = models.CharField(
        max_length=4,
        choices=SUPPORTED_COMPILERS,
        editable=False
    )
    status = models.SmallIntegerField(editable=False)
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
    # TODO Need test
    @classmethod
    def generate(cls, user, problem, language_suffix, source_code):
        user = None  # FIXME Get a user and save it?
        judge_information = problem.get_problem_config()
        judge_information['source_code'] = source_code
        judge_information['language_suffix'] = language_suffix
        judge_results = judge(**judge_information)
        record = cls.records_set.create(
            user=user,
            problem=problem,
            language=language_suffix,
            source_code=source_code,
            submit_time=datetime.now(),
            # TODO Add running time and memory cost
            # running_time = models.DurationField(editable=False)
            # memory_cost = models. ...
        )
        assert judge_results, "Error, judge results should never be empty."
        if judge_results[0] == JudgeResult.CE:
            record.status = JudgeResult.CE.value
        for judge_result, test_case in zip(judge_results,
                                           problem.testcase_set.all()
                                           ):
            record.testcaseresult_set.create(
                status=judge_result.value,
                test_case=test_case,
            )

    def get_result(self) -> str:
        pass

    def is_accepted(self) -> bool:
        return self.get_result is JudgeResult.AC
    is_accepted.admin_order_field = 'Accepted'
    is_accepted.boolean = True
    is_accepted.short_description = 'Is accepted'


class TestCaseResult(models.Model):
    status = models.SmallIntegerField(editable=False)
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    test_case = models.ForeignKey(
        "problems.TestCase",
        on_delete=models.CASCADE
    )
