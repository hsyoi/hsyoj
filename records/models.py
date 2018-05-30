from django.db import models

from common.compiler import SUPPORTED_LANGUAGE


class Record(models.Model):
    records_set = models.Manager()

    # user = models.ForeignKey(
    #     "User", on_delete=models.CASCADE, editable=False)
    problem = models.ForeignKey(
        "problems.Problem", on_delete=models.SET_NULL, null=True, editable=False)
    language = models.CharField(
        max_length=4, choices=SUPPORTED_LANGUAGE, editable=False)
    code = models.TextField(editable=False)
    submit_time = models.DateTimeField(auto_now_add=True, editable=False)
    running_time = models.DurationField(editable=False)

    @staticmethod
    def generate(user, problem, language, code):
        # TODO: Generate a recode from args
        raise NotImplementedError("TODO in records/models.py")
