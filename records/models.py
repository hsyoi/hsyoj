import uuid

from django.db import models

from common.compiler import SUPPORTED_COMPILERS
from common.judge import JudgeResult


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

    def get_result(self) -> JudgeResult:
        if self.is_accepted():
            return JudgeResult.AC
        for result in self.testcaseresult_set.all():
            if result.result_code != 0:
                return JudgeResult(result.result_code)

        raise RuntimeError(
            "No test case has been added or "
            "every test case results is AC "
            "but the result is not AC."
        )

    def is_accepted(self) -> bool:
        return bool(self.accepted_flag)

    is_accepted.admin_order_field = 'Accepted'
    is_accepted.boolean = True
    is_accepted.short_description = 'Is accepted'


class TestCaseResult(models.Model):
    result_code = models.SmallIntegerField(editable=False)
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    test_case = models.ForeignKey(
        "problems.TestCase",
        on_delete=models.SET_NULL,
        null=True,  # set test_case to null when result is CE
    )
